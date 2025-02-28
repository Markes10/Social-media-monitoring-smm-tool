import React, { useState } from "react";
import { View, TextInput, Button, Text, ScrollView } from "react-native";
import axios from "axios";

const ChatbotScreen = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const askChatbot = async () => {
    try {
      const res = await axios.post("http://your-api-url/chat", { query });
      setResponse(res.data.response);
    } catch (error) {
      console.error("Chatbot error:", error);
      setResponse("Error fetching response.");
    }
  };

  return (
    <View>
      <Text>Ask about social media trends:</Text>
      <TextInput 
        placeholder="Enter your question" 
        value={query} 
        onChangeText={setQuery} 
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }} 
      />
      <Button title="Ask Chatbot" onPress={askChatbot} />
      <ScrollView style={{ marginTop: 10 }}>
        <Text>{response}</Text>
      </ScrollView>
    </View>
  );
};

export default ChatbotScreen;
