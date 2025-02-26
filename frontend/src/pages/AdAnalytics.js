import React, { useState } from "react";
import { View, Text, Button, Picker, StyleSheet } from "react-native";
import axios from "axios";

const AdAnalytics = () => {
    const [platform, setPlatform] = useState("facebook");
    const [adData, setAdData] = useState(null);

    const fetchAdData = async () => {
        const apiUrl = `http://your-api-url/ads/${platform}`;
        const response = await axios.get(apiUrl);
        setAdData(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Ad Performance & ROI</Text>

            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Facebook Ads" value="facebook" />
                <Picker.Item label="Google Ads" value="google" />
                <Picker.Item label="Twitter Ads" value="twitter" />
            </Picker>

            <Button title="🚀 Fetch Ad Performance" onPress={fetchAdData} />

            {adData && (
                <View>
                    <Text style={styles.subHeader}>Ad Performance:</Text>
                    <Text>Impressions: {adData.impressions}</Text>
                    <Text>Clicks: {adData.clicks}</Text>
                    <Text>Spend: ${adData.spend}</Text>
                    <Text>Conversion Rate: {adData.conversion_rate}%</Text>
                </View>
            )}
        </View>
    );
};

export default AdAnalytics;
