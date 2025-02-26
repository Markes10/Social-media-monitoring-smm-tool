import React, { useState } from "react";
import { View, Text, TextInput, Button, Picker, StyleSheet } from "react-native";
import axios from "axios";

const InfluencerFinder = () => {
    const [platform, setPlatform] = useState("instagram");
    const [username, setUsername] = useState("");
    const [influencerData, setInfluencerData] = useState(null);

    const fetchInfluencerData = async () => {
        const apiUrl = platform === "instagram"
            ? `http://your-api-url/influencer/instagram?username=${username}`
            : `http://your-api-url/influencer/twitter?handle=${username}`;
        
        const response = await axios.get(apiUrl);
        setInfluencerData(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🔍 Influencer Finder</Text>

            <TextInput
                placeholder="Enter Influencer Username"
                value={username}
                onChangeText={setUsername}
                style={styles.input}
            />

            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Instagram" value="instagram" />
                <Picker.Item label="Twitter" value="twitter" />
            </Picker>

            <Button title="📊 Fetch Influencer Data" onPress={fetchInfluencerData} />

            {influencerData && (
                <View>
                    <Text style={styles.subHeader}>Influencer Stats:</Text>
                    <Text>Followers: {influencerData.followers}</Text>
                    <Text>Engagement Rate: {influencerData.engagement_rate}%</Text>
                    <Text>Posts/Tweets: {influencerData.posts || influencerData.tweets}</Text>
                </View>
            )}
        </View>
    );
};

export default InfluencerFinder;
