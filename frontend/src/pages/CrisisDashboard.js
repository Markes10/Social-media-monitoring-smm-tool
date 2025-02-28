import React, { useState, useEffect } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import axios from "axios";

const CrisisDashboard = () => {
    const [crisisData, setCrisisData] = useState(null);

    const fetchCrisisAlerts = async () => {
        const response = await axios.get("http://your-api-url/crisis-detection");
        setCrisisData(response.data.crisis_data);
    };

    useEffect(() => {
        fetchCrisisAlerts();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🚨 AI-Powered Crisis Detection</Text>
            
            {crisisData && crisisData.crisis_detected ? (
                crisisData.alerts.map((alert, index) => (
                    <View key={index}>
                        <Text>⚠️ Alert Level: {alert.alert_level}</Text>
                        <Text>📝 Post: "{alert.text}"</Text>
                        <Text>⏰ Timestamp: {alert.timestamp}</Text>
                        <Text>💡 Recommendation: {alert.recommendation}</Text>
                    </View>
                ))
            ) : (
                <Text>✅ No Crisis Detected</Text>
            )}
            
            <Button title="Refresh Crisis Alerts" onPress={fetchCrisisAlerts} />
        </View>
    );
};

export default CrisisDashboard;
