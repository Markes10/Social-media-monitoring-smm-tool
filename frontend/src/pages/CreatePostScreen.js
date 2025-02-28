import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const CreatePostScreen = () => {
    const [content, setContent] = useState("");
    const [hashtags, setHashtags] = useState("");
    const [suggestedPosts, setSuggestedPosts] = useState([]);

    const generateHashtags = async () => {
        const response = await axios.post("http://your-api-url/generate-hashtags", { content });
        setHashtags(response.data.hashtags);
    };

    const fetchPostSuggestions = async () => {
        const response = await axios.get("http://your-api-url/generate-posts");
        setSuggestedPosts(response.data.post_suggestions.split("\n"));
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>Create a New Post</Text>
            
            <TextInput 
                style={styles.input}
                placeholder="Write your post here..."
                value={content}
                onChangeText={setContent}
            />

            <Button title="Generate Hashtags" onPress={generateHashtags} />
            <Text style={styles.hashtags}>{hashtags}</Text>

            <Button title="Get AI Suggestions" onPress={fetchPostSuggestions} />
            {suggestedPosts.map((post, index) => (
                <Text key={index} style={styles.suggestion}>{post}</Text>
            ))}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
    input: { borderWidth: 1, padding: 10, marginVertical: 10 },
    hashtags: { fontWeight: "bold", marginVertical: 5 },
    suggestion: { fontStyle: "italic", marginVertical: 5 },
});

export default CreatePostScreen;
