import React, { useState } from "react";
import { View, Text, Button } from "react-native";
import axios from "axios";

const AdOptimizationDashboard = () => {
    const [data, setData] = useState(null);

    const fetchOptimizations = async () => {
        const res = await axios.get("http://your-api-url/optimize_ads");
        setData(res.data);
    };

    return (
        <View>
            <Text>🎯 AI-Powered Ad Optimization</Text>
            <Button title="📊 Optimize Ads" onPress={fetchOptimizations} />

            {data && (
                <View>
                    <Text>🚀 AI Optimization Suggestions: {data.ad_optimization}</Text>
                </View>
            )}
        </View>
    );
};

export default AdOptimizationDashboard;
