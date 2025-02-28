import React, { useState } from "react";
import { View, Text, Button } from "react-native";
import axios from "axios";

const AdPersonalizationDashboard = () => {
    const [data, setData] = useState(null);

    const fetchPersonalizedAds = async () => {
        const res = await axios.get("http://your-api-url/personalize_ads");
        setData(res.data);
    };

    return (
        <View>
            <Text>🎯 AI-Powered Personalized Ads</Text>
            <Button title="📊 Generate Personalized Ads" onPress={fetchPersonalizedAds} />

            {data && (
                <View>
                    <Text>🚀 AI Recommendations: {data.personalized_ads}</Text>
                </View>
            )}
        </View>
    );
};

export default AdPersonalizationDashboard;
