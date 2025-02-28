import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const InfluencerMonitor = () => {
    const [platform, setPlatform] = useState("twitter");
    const [keyword, setKeyword] = useState("");
    const [influencers, setInfluencers] = useState([]);

    const fetchInfluencers = async () => {
        const response = await axios.get(`http://your-api-url/influencers?platform=${platform}&keyword=${keyword}`);
        setInfluencers(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🤝 Influencer Discovery</Text>

            <TextInput
                placeholder="Enter keyword (e.g. fitness, tech, fashion)"
                value={keyword}
                onChangeText={setKeyword}
                style={styles.input}
            />

            <Button title="🔍 Find Influencers" onPress={fetchInfluencers} />
            
            <FlatList
                data={influencers}
                renderItem={({ item }) => <Text>🔥 {item.id} (Mentions: {item.mentions})</Text>}
                keyExtractor={(item, index) => index.toString()}
            />
        </View>
    );
};

export default InfluencerMonitor;
