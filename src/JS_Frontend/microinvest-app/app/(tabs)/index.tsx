import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Platform,
  Dimensions,
  SafeAreaView,
  StatusBar
} from 'react-native';
import { Ionicons, MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

type Portfolio = {
  total_invested: number;
  portfolio_value: number;
  nominal_roi: number;
  real_roi: number;
};

// Placeholder data for transactions
const TRANSACTIONS = [
  {
    id: '1',
    title: 'Salary',
    date: '18:27 - April 30',
    category: 'Monthly',
    amount: 4000.00,
    icon: 'cash', // Ionicons
    color: '#60A5FA', // Blue
  },
  {
    id: '2',
    title: 'Groceries',
    date: '17:00 - April 24',
    category: 'Pantry',
    amount: -100.00,
    icon: 'basket', // Ionicons
    color: '#3B82F6', // Blue
  },
  {
    id: '3',
    title: 'Rent',
    date: '8:30 - April 15',
    category: 'Rent',
    amount: -674.40,
    icon: 'home', // Ionicons
    color: '#2563EB', // Darker Blue
  },
];

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('Monthly');

  // Detect platform and set API URL
  const API_URL = Platform.OS === 'web'
    ? "http://localhost:5000"
    : "http://10.0.2.2:5000";

  const fetchPortfolio = async () => {
    try {
      const res = await fetch(`${API_URL}/portfolio`);
      if (!res.ok) return;
      const data = await res.json();
      setPortfolio(data);
    } catch (err) {
      console.error("fetchPortfolio execution error:", err);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchPortfolio();
  }, []);

  const formatCurrency = (value: number) => {
    return value.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    });
  };

  return (
    <View style={styles.container}>
      {/* Upper Green Section */}
      <View style={[styles.headerContainer, { paddingTop: insets.top + 10 }]}>
        <View style={styles.headerTopRow}>
          <View>
            <Text style={styles.greetingText}>Hi, Welcome Back</Text>
            <Text style={styles.subGreetingText}>Good Morning</Text>
          </View>
          <TouchableOpacity style={styles.notificationButton}>
            <Ionicons name="notifications-outline" size={24} color="#004D40" />
          </TouchableOpacity>
        </View>

        {/* Portfolio Summary */}
        <View style={styles.portfolioRow}>
          <View style={styles.portfolioItem}>
            <View style={styles.portfolioLabelRow}>
              <MaterialCommunityIcons name="arrow-top-right" size={16} color="#004D40" />
              <Text style={styles.portfolioLabel}> Portfolio Value</Text>
            </View>
            <Text style={styles.portfolioValue}>
              {portfolio ? formatCurrency(portfolio.portfolio_value) : '$...'}
            </Text>
          </View>

          <View style={styles.verticalDivider} />

          <View style={styles.portfolioItem}>
            <View style={styles.portfolioLabelRow}>
              <MaterialCommunityIcons name="arrow-bottom-right" size={16} color="#004D40" />
              <Text style={styles.portfolioLabel}> Total Invested</Text>
            </View>
            <Text style={styles.totalInvestedValue}>
              {portfolio ? formatCurrency(portfolio.total_invested) : '$...'}
            </Text>
          </View>
        </View>

        {/* Progress Bar Plugin */}
        <View style={styles.progressSection}>
          <View style={styles.progressBarContainer}>
            <View style={[styles.progressBarFill, { width: '30%' }]}>
              <Text style={styles.progressText}>30%</Text>
            </View>
            <View style={styles.progressRest}>
              <Text style={styles.progressTotal}>$20,000.00</Text>
            </View>
          </View>
          <View style={styles.progressMessageRow}>
            <Ionicons name="checkbox-outline" size={16} color="#004D40" />
            <Text style={styles.progressMessage}> 30% Of Your Expenses, Looks Good.</Text>
          </View>
        </View>

      </View>

      {/* Main Content (White/Light Area) */}
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Statistics Card (Green Card) */}
        <View style={styles.statsCard}>
          {/* Left Side: Circular Progress */}
          <View style={styles.circularProgressContainer}>
            <View style={styles.circleOuter}>
              <Ionicons name="car-sport-outline" size={28} color="#004D40" />
            </View>
            <Text style={styles.savingsText}>Savings</Text>
            <Text style={styles.savingsText}>On Goals</Text>
          </View>

          <View style={styles.statsDivider} />

          {/* Right Side: Stats List */}
          <View style={styles.statsList}>
            <View style={styles.statItem}>
              <View style={styles.iconBox}>
                <FontAwesome5 name="money-bill-wave" size={18} color="#004D40" />
              </View>
              <View>
                <Text style={styles.statLabel}>Revenue Last Week</Text>
                <Text style={styles.statValue}>$4,000.00</Text>
              </View>
            </View>
            <View style={styles.horizontalLine} />
            <View style={styles.statItem}>
              <View style={styles.iconBox}>
                <MaterialCommunityIcons name="silverware-fork-knife" size={18} color="#004D40" />
              </View>
              <View>
                <Text style={styles.statLabel}>Food Last Week</Text>
                <Text style={styles.statNegativeValue}>-$100.00</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Tab Filters */}
        <View style={styles.tabsContainer}>
          {['Daily', 'Weekly', 'Monthly'].map((tab) => (
            <TouchableOpacity
              key={tab}
              style={[styles.tabButton, activeTab === tab && styles.activeTabButton]}
              onPress={() => setActiveTab(tab)}
            >
              <Text style={[styles.tabText, activeTab === tab && styles.activeTabText]}>
                {tab}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Transactions List */}
        <View style={styles.transactionsList}>
          {TRANSACTIONS.map((item) => (
            <View key={item.id} style={styles.transactionRow}>
              <View style={[styles.transactionIconBg, { backgroundColor: item.color }]}>
                <Ionicons name={item.icon as any} size={24} color="#FFF" />
              </View>
              <View style={styles.transactionInfo}>
                <Text style={styles.transactionTitle}>{item.title}</Text>
                <Text style={styles.transactionDate}>{item.date}</Text>
              </View>
              <View style={[styles.verticalLine, { backgroundColor: '#4FD1C5' }]} />
              <View style={styles.transactionCategory}>
                <Text style={styles.categoryText}>{item.category}</Text>
              </View>
              <View style={[styles.verticalLine, { backgroundColor: '#4FD1C5' }]} />

              <Text style={[
                styles.transactionAmount,
                item.amount > 0 ? styles.amountPositive : styles.amountNegative
              ]}>
                {item.amount > 0 ? '' : ''}{formatCurrency(item.amount)}
              </Text>
            </View>
          ))}
        </View>

        {/* Bottom padding for tab bar */}
        <View style={{ height: 80 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F0FDF9', // Very light mint background
  },
  headerContainer: {
    backgroundColor: '#05C28F', // Main Green
    paddingHorizontal: 24,
    paddingBottom: 40,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  headerTopRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  greetingText: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#00382E',
  },
  subGreetingText: {
    fontSize: 14,
    color: '#004D40',
    opacity: 0.8,
  },
  notificationButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  portfolioRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 20,
  },
  portfolioItem: {
    flex: 1,
  },
  portfolioLabelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  portfolioLabel: {
    color: '#004D40',
    fontSize: 13,
    fontWeight: '500',
  },
  portfolioValue: {
    fontSize: 28,
    fontWeight: 'bold',
    // Let's use a dark blue/purple to match the contrast in wireframe "7500.00"
    color: '#1E3A8A', // Dark Blue
  },
  totalInvestedValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF', // White for the second value
  },
  verticalDivider: {
    width: 1,
    height: 40,
    backgroundColor: 'rgba(0,0,0,0.1)',
    marginHorizontal: 16,
    alignSelf: 'center',
  },
  progressSection: {
    marginTop: 8,
  },
  progressBarContainer: {
    flexDirection: 'row',
    backgroundColor: '#E0F2F1', // Light background for bar
    borderRadius: 20,
    height: 36,
    alignItems: 'center',
    padding: 2,
    marginBottom: 8,
  },
  progressBarFill: {
    backgroundColor: '#00382E', // Dark Green
    height: '100%',
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  progressRest: {
    flex: 1,
    alignItems: 'flex-end',
    paddingRight: 16,
  },
  progressText: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 12,
  },
  progressTotal: {
    color: '#004D40',
    fontWeight: 'bold',
    fontSize: 14,
  },
  progressMessageRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  progressMessage: {
    marginLeft: 6,
    color: '#00382E',
    fontSize: 13,
    fontWeight: '500',
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 24,
  },
  statsCard: {
    backgroundColor: '#05C28F',
    borderRadius: 24,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
    shadowColor: '#05C28F',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    elevation: 6,
  },
  circularProgressContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingRight: 16,
  },
  circleOuter: {
    width: 60,
    height: 60,
    borderRadius: 30,
    borderWidth: 3,
    borderColor: '#3B82F6', // Blue ring
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 4,
  },
  savingsText: {
    color: '#00382E',
    fontSize: 11,
    fontWeight: '600',
    textAlign: 'center',
  },
  statsDivider: {
    width: 1,
    height: 60,
    backgroundColor: 'rgba(255,255,255,0.3)',
    marginRight: 16,
  },
  statsList: {
    flex: 1,
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  iconBox: {
    marginRight: 12,
    width: 32,
    alignItems: 'center'
  },
  statLabel: {
    color: '#004D40',
    fontSize: 12,
    marginBottom: 2,
  },
  statValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#00382E',
  },
  statNegativeValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1E40AF', // Blue
  },
  horizontalLine: {
    height: 1,
    backgroundColor: 'rgba(255,255,255,0.3)',
    marginVertical: 6,
    width: '80%',
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: '#E6F4F1',
    borderRadius: 20,
    padding: 4,
    marginBottom: 24,
  },
  tabButton: {
    flex: 1,
    paddingVertical: 10,
    alignItems: 'center',
    borderRadius: 16,
  },
  activeTabButton: {
    backgroundColor: '#00C48C', // Bright Green
  },
  tabText: {
    color: '#555',
    fontWeight: '600',
  },
  activeTabText: {
    color: '#00382E',
  },
  transactionsList: {
    gap: 16,
  },
  transactionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF',
    padding: 16, // Reduced padding
    borderRadius: 20, // More rounded
    // No shadow in wireframe maybe? Adding subtle one
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
    marginBottom: 12,
  },
  transactionIconBg: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  transactionInfo: {
    flex: 2,
  },
  transactionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  transactionDate: {
    fontSize: 12,
    color: '#3B82F6', // Blue as in wireframe
    fontWeight: '500',
  },
  verticalLine: {
    width: 1,
    height: 30,
    backgroundColor: '#E5E7EB',
    marginHorizontal: 10,
  },
  transactionCategory: {
    flex: 1,
    alignItems: 'center',
  },
  categoryText: {
    fontSize: 12,
    color: '#666',
  },
  transactionAmount: {
    fontSize: 16,
    fontWeight: 'bold',
    minWidth: 80,
    textAlign: 'right',
  },
  amountPositive: {
    color: '#333',
  },
  amountNegative: {
    color: '#2563EB',
  },
});

