import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';

const QUICK_AMOUNTS = [50, 100, 500];

export default function InvestScreen({ navigation }) {
  const [walletBalance, setWalletBalance] = useState(500); // Replace with API call
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleQuickSelect = (amt: number) => {
    setAmount(amt.toString());
  };

  const handleInvest = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:5000/invest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: Number(amount), fund_id: 'fund_001' }),
      });
      if (res.status === 201) {
        // Refresh wallet and portfolio (replace with actual API calls)
        setWalletBalance(walletBalance - Number(amount));
        // navigation.goBack(); // Or navigate to portfolio
      } else {
        const data = await res.json();
        setError(data.error || 'Investment failed');
      }
    } catch (e) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.balance}>Wallet Balance: ₹{walletBalance}</Text>
      <Text style={styles.label}>Enter Investment Amount</Text>
      <TextInput
        style={styles.input}
        keyboardType="numeric"
        value={amount}
        onChangeText={setAmount}
        placeholder="Amount"
      />
      <View style={styles.quickRow}>
        {QUICK_AMOUNTS.map((amt) => (
          <TouchableOpacity key={amt} style={styles.quickBtn} onPress={() => handleQuickSelect(amt)}>
            <Text style={styles.quickText}>₹{amt}</Text>
          </TouchableOpacity>
        ))}
      </View>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <TouchableOpacity style={styles.confirmBtn} onPress={handleInvest} disabled={loading || !amount}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.confirmText}>Confirm Investment</Text>}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#fff',
  },
  balance: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 16,
  },
  quickRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  quickBtn: {
    backgroundColor: '#e0e0e0',
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 18,
  },
  quickText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  confirmBtn: {
    backgroundColor: '#1976d2',
    borderRadius: 8,
    paddingVertical: 14,
    alignItems: 'center',
  },
  confirmText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  error: {
    color: 'red',
    marginBottom: 12,
  },
});
