import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const AdPerformanceDashboard = () => {
    const [platform, setPlatform] = useState("");
    const [data, setData] = useState(null);

    const fetchAdPerformance = async () => {
        const res = await axios.get(`http://your-api-url/ad_optimization?platform=${platform}`);
        setData(res.data);
    };

    return (
        <View>
            <Text>📊 Ad Performance & Optimization</Text>
            <TextInput
                placeholder="Enter platform (Facebook, Google Ads, etc.)"
                value={platform}
                onChangeText={setPlatform}
            />
            <Button title="🔍 Optimize Ads" onPress={fetchAdPerformance} />

            {data && (
                <View>
                    <Text>📢 AI Recommendations: {data.recommendations}</Text>
                    <Text>📊 Ad Data: {JSON.stringify(data.ad_performance, null, 2)}</Text>
                </View>
            )}
        </View>
    );
};

export default AdPerformanceDashboard;
