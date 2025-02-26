import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const AdPerformanceDashboard = () => {
    const [budget, setBudget] = useState("");
    const [audience, setAudience] = useState("");
    const [ctr, setCtr] = useState("");
    const [prediction, setPrediction] = useState(null);

    const predictPerformance = async () => {
        const response = await axios.post("http://your-api-url/predict-ad-performance", {
            budget: parseFloat(budget),
            target_audience: parseInt(audience),
            past_ctr: parseFloat(ctr),
        });
        setPrediction(response.data.predicted_conversions);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 AI Ad Performance Prediction</Text>

            <TextInput
                placeholder="💰 Ad Budget ($)"
                value={budget}
                onChangeText={setBudget}
                keyboardType="numeric"
                style={styles.input}
            />
            <TextInput
                placeholder="👥 Target Audience Size"
                value={audience}
                onChangeText={setAudience}
                keyboardType="numeric"
                style={styles.input}
            />
            <TextInput
                placeholder="📈 Past CTR (%)"
                value={ctr}
                onChangeText={setCtr}
                keyboardType="numeric"
                style={styles.input}
            />

            <Button title="🔮 Predict Conversions" onPress={predictPerformance} />

            {prediction !== null && (
                <Text style={styles.result}>🎯 Predicted Conversions: {prediction}</Text>
            )}
        </View>
    );
};

export default AdPerformanceDashboard;
