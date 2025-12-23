import { Text, View, Button, StyleSheet, Platform } from "react-native";
import { useEffect, useState } from "react";

type Portfolio = {
  total_invested: number;
  portfolio_value: number;
  nominal_roi: number;
  real_roi: number;
};

export default function HomeScreen() {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);

  // Detect platform and set API URL
  const API_URL = Platform.OS === 'web'
    ? "http://localhost:5000"
    : "http://10.0.2.2:5000";

  const fetchPortfolio = async () => {
    console.log(`[mn] Starting fetchPortfolio from: ${API_URL}/portfolio`);
    try {
      const res = await fetch(`${API_URL}/portfolio`);
      console.log(`[mn] fetchPortfolio status: ${res.status}`);

      if (!res.ok) {
        console.error(`[mn] fetchPortfolio HTTP error! status: ${res.status}`);
        return;
      }

      const data = await res.json();
      console.log('[mn] fetchPortfolio data:', data);
      setPortfolio(data);
    } catch (err) {
      console.error("[mn] fetchPortfolio execution error:", err);
    } finally {
      setLoading(false);
      console.log('[mn] fetchPortfolio finished, loading set to false');
    }
  };

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const invest = async () => {
    console.log(`[mn] Starting invest call to: ${API_URL}/invest`);
    try {
      const res = await fetch(`${API_URL}/invest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          amount: 10,
          fund_id: "LIQUID_001",
        }),
      });

      console.log(`[mn] invest status: ${res.status}`);

      if (res.ok) {
        console.log('[mn] invest success, refreshing portfolio...');
        fetchPortfolio(); // refresh dashboard
      } else {
        const errorText = await res.text();
        console.error('[mn] invest failed response:', errorText);
      }
    } catch (err) {
      console.error("[mn] invest execution error:", err);
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <Text style={styles.text}>Loading portfolio...</Text>
      </View>
    );
  }

  if (!portfolio) {
    return (
      <View style={styles.center}>
        <Text style={styles.text}>Failed to load portfolio</Text>
        <Button title="Retry" onPress={fetchPortfolio} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dashboard</Text>

      <Text style={styles.text}>Total Invested: ${portfolio.total_invested}</Text>
      <Text style={styles.text}>Portfolio Value: ${portfolio.portfolio_value}</Text>
      <Text style={styles.text}>Nominal ROI: {portfolio.nominal_roi}%</Text>
      <Text style={styles.text}>Real ROI: {portfolio.real_roi}%</Text>

      <Button title="Invest $10" onPress={invest} />
    </View>
  );
}

const styles = StyleSheet.create({
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: '#ffffff',
  },
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    backgroundColor: '#ffffff',
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: '#000000',
  },
  text: {
    fontSize: 16,
    color: '#000000',
    marginVertical: 5,
  },
});
