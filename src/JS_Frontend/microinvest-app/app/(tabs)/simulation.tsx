import React, { useEffect, useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    Platform,
    Dimensions,
    SafeAreaView,
    ScrollView,
    StatusBar
} from 'react-native';
import { MaterialCommunityIcons, Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

type Portfolio = {
    total_invested: number;
    portfolio_value: number;
    nominal_roi: number;
    real_roi: number;
};

export default function SimulationScreen() {
    const insets = useSafeAreaInsets();
    const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
    const [loading, setLoading] = useState(false);

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
            console.error("fetchPortfolio error:", err);
        }
    };

    const handleSimulate = async () => {
        try {
            setLoading(true);
            const res = await fetch(`${API_URL}/simulate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ days: 30 }),
            });

            if (res.ok) {
                // Refresh portfolio to see new values
                await fetchPortfolio();
            }
        } catch (err) {
            console.error("Simulation failed:", err);
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
            {/* Header */}
            <View style={[styles.headerContainer, { paddingTop: insets.top + 20 }]}>
                <Text style={styles.headerTitle}>Demo Simulation</Text>
                <Text style={styles.headerSubtitle}>Test the power of compounding</Text>
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                {/* Simulation Card */}
                <View style={styles.card}>
                    <View style={styles.cardHeader}>
                        <MaterialCommunityIcons name="flask-outline" size={24} color="#004D40" />
                        <Text style={styles.cardTitle}>Current Simulation State</Text>
                    </View>

                    <View style={styles.divider} />

                    <View style={styles.metricRow}>
                        <Text style={styles.metricLabel}>Simulated Portfolio Value</Text>
                        <Text style={styles.metricValue}>
                            {portfolio ? formatCurrency(portfolio.portfolio_value) : '$...'}
                        </Text>
                    </View>

                    <View style={styles.metricRow}>
                        <Text style={styles.metricLabel}>Nominal ROI</Text>
                        <Text style={[styles.metricValue, { color: '#059669' }]}>
                            {portfolio ? `${portfolio.nominal_roi.toFixed(2)}%` : '...%'}
                        </Text>
                    </View>
                </View>

                {/* Action Section */}
                <View style={styles.actionContainer}>
                    <Text style={styles.description}>
                        Advance time by 30 days to see how daily compounding affects your portfolio.
                        This action runs on the backend engine.
                    </Text>

                    <TouchableOpacity
                        style={[styles.simulateButton, loading && styles.buttonDisabled]}
                        onPress={handleSimulate}
                        disabled={loading}
                    >
                        {loading ? (
                            <Text style={styles.buttonText}>Simulating...</Text>
                        ) : (
                            <>
                                <MaterialCommunityIcons name="clock-fast" size={20} color="#FFF" style={{ marginRight: 8 }} />
                                <Text style={styles.buttonText}>Simulate 30 Days</Text>
                            </>
                        )}
                    </TouchableOpacity>
                </View>

                {/* Disclaimer */}
                <View style={styles.disclaimerContainer}>
                    <Ionicons name="information-circle-outline" size={20} color="#888" style={{ marginRight: 6 }} />
                    <Text style={styles.disclaimerText}>
                        This is a meaningful demo simulation. It assumes 8% APY daily compounding.
                        Changes affect the backend engine state but are for demonstration purposes only.
                    </Text>
                </View>
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F0FDF9',
    },
    headerContainer: {
        paddingHorizontal: 24,
        paddingBottom: 24,
        backgroundColor: '#FFFFFF',
        borderBottomLeftRadius: 24,
        borderBottomRightRadius: 24,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        shadowRadius: 8,
        elevation: 4,
        marginBottom: 20,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#004D40',
    },
    headerSubtitle: {
        fontSize: 14,
        color: '#666',
        marginTop: 4,
    },
    content: {
        paddingHorizontal: 20,
        paddingBottom: 40,
    },
    card: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 24,
        marginBottom: 24,
        shadowColor: '#004D40',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 12,
        elevation: 4,
    },
    cardHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 16,
    },
    cardTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#004D40',
        marginLeft: 12,
    },
    divider: {
        height: 1,
        backgroundColor: '#F0F0F0',
        marginBottom: 16,
    },
    metricRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12,
    },
    metricLabel: {
        fontSize: 14,
        color: '#666',
    },
    metricValue: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#333',
    },
    actionContainer: {
        backgroundColor: '#E0F2F1',
        borderRadius: 20,
        padding: 24,
        marginBottom: 24,
        alignItems: 'center',
    },
    description: {
        textAlign: 'center',
        color: '#004D40',
        marginBottom: 20,
        lineHeight: 20,
        fontSize: 14,
    },
    simulateButton: {
        backgroundColor: '#05C28F',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 16,
        paddingHorizontal: 32,
        borderRadius: 30,
        width: '100%',
        shadowColor: '#05C28F',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 6,
    },
    buttonDisabled: {
        opacity: 0.7,
    },
    buttonText: {
        color: '#FFFFFF',
        fontWeight: 'bold',
        fontSize: 16,
    },
    disclaimerContainer: {
        flexDirection: 'row',
        backgroundColor: '#F3F4F6',
        padding: 16,
        borderRadius: 12,
        alignItems: 'flex-start',
    },
    disclaimerText: {
        flex: 1,
        fontSize: 12,
        color: '#888',
        lineHeight: 18,
    },
});
