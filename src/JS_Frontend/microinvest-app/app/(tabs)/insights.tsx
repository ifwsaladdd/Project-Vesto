import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Platform, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

type Insights = {
    idle_money_loss: number;
    daily_vs_periodic_gain: number;
    inflation_message: string;
    disclaimer: string;
};

export default function InsightsScreen() {
    const insets = useSafeAreaInsets();
    const [insights, setInsights] = useState<Insights | null>(null);
    const [loading, setLoading] = useState(true);

    const API_URL = Platform.OS === 'web'
        ? "http://localhost:5000"
        : "http://10.0.2.2:5000";

    const fetchInsights = async () => {
        try {
            const res = await fetch(`${API_URL}/insights`);
            if (!res.ok) return;
            const data = await res.json();
            setInsights(data);
        } catch (err) {
            console.error("fetchInsights execution error:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchInsights();
    }, []);

    if (loading) {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#004D40" />
                <Text style={styles.loadingText}>Gathering insights...</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {/* Header */}
            <View style={[styles.headerContainer, { paddingTop: insets.top + 10 }]}>
                <Text style={styles.headerTitle}>Financial Insights</Text>
                <Text style={styles.headerSubtitle}>Understand your money better</Text>
            </View>

            <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
                {insights ? (
                    <>
                        {/* Inflation Card */}
                        <View style={styles.card}>
                            <View style={styles.cardHeader}>
                                <View style={[styles.iconContainer, { backgroundColor: '#FEE2E2' }]}>
                                    <Ionicons name="trending-down" size={24} color="#EF4444" />
                                </View>
                                <Text style={styles.cardTitle}>Inflation Impact</Text>
                            </View>
                            <Text style={styles.cardBody}>
                                {insights.inflation_message}
                            </Text>
                        </View>

                        {/* Idle Money Card */}
                        <View style={styles.card}>
                            <View style={styles.cardHeader}>
                                <View style={[styles.iconContainer, { backgroundColor: '#FEF3C7' }]}>
                                    <Ionicons name="wallet-outline" size={24} color="#D97706" />
                                </View>
                                <Text style={styles.cardTitle}>Idle Money</Text>
                            </View>
                            <Text style={styles.cardBody}>
                                You have approximately <Text style={styles.boldAmount}>${insights.idle_money_loss.toFixed(2)}</Text> in effective purchasing power currently sitting idle or lost to inflation compared to real value.
                            </Text>
                        </View>

                        {/* Disclaimer */}
                        <View style={styles.disclaimerContainer}>
                            <Ionicons name="information-circle-outline" size={16} color="#666" />
                            <Text style={styles.disclaimerText}>{insights.disclaimer}</Text>
                        </View>
                    </>
                ) : (
                    <View style={styles.errorContainer}>
                        <Text style={styles.errorText}>Unavailable to load insights right now.</Text>
                    </View>
                )}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F0FDF9',
    },
    center: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F0FDF9',
    },
    loadingText: {
        marginTop: 12,
        fontSize: 16,
        color: '#004D40',
    },
    headerContainer: {
        backgroundColor: '#05C28F',
        paddingHorizontal: 24,
        paddingBottom: 32,
        borderBottomLeftRadius: 30,
        borderBottomRightRadius: 30,
        marginBottom: 16,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#00382E',
    },
    headerSubtitle: {
        fontSize: 16,
        color: '#004D40',
        opacity: 0.9,
        marginTop: 4,
    },
    scrollContent: {
        padding: 20,
        paddingTop: 10,
    },
    card: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 20,
        marginBottom: 20,
        shadowColor: '#05C28F',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 10,
        elevation: 4,
    },
    cardHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 12,
    },
    iconContainer: {
        width: 48,
        height: 48,
        borderRadius: 24,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 16,
    },
    cardTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333',
    },
    cardBody: {
        fontSize: 16,
        color: '#4B5563',
        lineHeight: 24,
    },
    boldAmount: {
        fontWeight: 'bold',
        color: '#111827',
    },
    disclaimerContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#E5E7EB',
        padding: 12,
        borderRadius: 12,
        marginTop: 8,
    },
    disclaimerText: {
        fontSize: 12,
        color: '#6B7280',
        marginLeft: 8,
        flex: 1,
        fontStyle: 'italic',
    },
    errorContainer: {
        alignItems: 'center',
        marginTop: 40,
    },
    errorText: {
        color: '#EF4444',
        fontSize: 16,
    },
});
