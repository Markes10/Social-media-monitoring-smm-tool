import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const InfluencerDashboard = () => {
    const [brand, setBrand] = useState("");
    const [category, setCategory] = useState("");
    const [influencers, setInfluencers] = useState([]);
    const [strategy, setStrategy] = useState(null);

    const fetchInfluencers = async () => {
        const res = await axios.get(`http://your-api-url/top_influencers?brand_handle=${brand}`);
        setInfluencers(res.data.influencers);
    };

    const fetchInfluencerStrategy = async () => {
        const res = await axios.get(`http://your-api-url/influencer_strategy?brand=${brand}&category=${category}`);
        setStrategy(res.data);
    };

    useEffect(() => {
        fetchInfluencers();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📢 Influencer Analysis & Collaboration Strategy</Text>

            <TextInput
                placeholder="Enter a brand name (e.g. Nike)"
                value={brand}
                onChangeText={setBrand}
                style={styles.input}
            />
            <Button title="🔍 Find Influencers" onPress={fetchInfluencers} />

            <FlatList
                data={influencers}
                keyExtractor={(item) => item.handle}
                renderItem={({ item }) => (
                    <View>
                        <Text>👤 @{item.handle} - Mentions: {item.mentions}</Text>
                    </View>
                )}
            />

            <TextInput
                placeholder="Enter category (e.g., Fitness, Tech, Fashion)"
                value={category}
                onChangeText={setCategory}
                style={styles.input}
            />
            <Button title="🤝 Get Collaboration Strategy" onPress={fetchInfluencerStrategy} />

            {strategy && (
                <View>
                    <Text>📢 AI Partnership Strategy: {strategy.partnership_strategy}</Text>
                    <Text>🔥 Top Influencers: {JSON.stringify(strategy.top_influencers, null, 2)}</Text>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
});

export default InfluencerDashboard;
