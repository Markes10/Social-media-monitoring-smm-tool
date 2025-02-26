import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const AdOptimizer = () => {
    const [adSpend, setAdSpend] = useState("");
    const [ctr, setCTR] = useState("");
    const [conversionRate, setConversionRate] = useState("");
    const [optimizedBudget, setOptimizedBudget] = useState(null);

    const fetchOptimization = async () => {
        const response = await axios.get(
            `http://your-api-url/ad-optimization?ad_spend=${adSpend}&ctr=${ctr}&conversion_rate=${conversionRate}`
        );
        setOptimizedBudget(response.data.optimized_budget);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📈 AI-Powered Ad Optimization</Text>
            <TextInput style={styles.input} placeholder="Ad Spend ($)" keyboardType="numeric" value={adSpend} onChangeText={setAdSpend} />
            <TextInput style={styles.input} placeholder="Click-Through Rate (%)" keyboardType="numeric" value={ctr} onChangeText={setCTR} />
            <TextInput style={styles.input} placeholder="Conversion Rate (%)" keyboardType="numeric" value={conversionRate} onChangeText={setConversionRate} />
            <Button title="Optimize Ad Budget" onPress={fetchOptimization} />

            {optimizedBudget && <Text style={styles.result}>💰 Suggested Budget: ${optimizedBudget.toFixed(2)}</Text>}
        </View>
    );
};

export default AdOptimizer;
