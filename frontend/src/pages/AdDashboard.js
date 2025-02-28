import React, { useState, useEffect } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import axios from "axios";

const AdDashboard = () => {
    const [adData, setAdData] = useState(null);

    const fetchAdOptimization = async () => {
        const response = await axios.get("http://your-api-url/ad-optimization");
        setAdData(response.data.ad_data);
    };

    useEffect(() => {
        fetchAdOptimization();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📈 AI-Powered Ad Optimization</Text>
            {adData ? (
                <View>
                    <Text>🏆 Best Campaign: {adData.best_campaign}</Text>
                    <Text>📊 Best CTR: {adData.best_ctr}%</Text>
                    <Text>💰 Best CPC: ${adData.best_cpc}</Text>
                    <Text>🚀 Best Conversion Rate: {adData.best_conversion_rate}%</Text>
                    <Text>💡 Recommendation: {adData.recommendation}</Text>
                </View>
            ) : (
                <Text>Loading ad performance insights...</Text>
            )}
        </View>
    );
};

export default AdDashboard;
