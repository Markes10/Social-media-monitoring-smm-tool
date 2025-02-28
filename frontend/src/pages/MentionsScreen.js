import React, { useState, useEffect } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const MentionsScreen = () => {
    const [mentions, setMentions] = useState([]);

    useEffect(() => {
        fetchMentions();
    }, []);

    const fetchMentions = async () => {
        const response = await axios.get("http://your-api-url/mentions");
        setMentions(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>Social Mentions</Text>

            <FlatList
                data={mentions}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.mention}>
                        <Text>📢 {item.platform}</Text>
                        <Text>👤 @{item.user_handle}</Text>
                        <Text>📝 {item.mention_text}</Text>
                        <Text>🔍 Sentiment: {item.sentiment}</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
    mention: { padding: 10, borderBottomWidth: 1, marginVertical: 5 },
});

export default MentionsScreen;
