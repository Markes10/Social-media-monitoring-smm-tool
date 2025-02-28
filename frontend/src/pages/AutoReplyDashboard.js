import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, ScrollView } from "react-native";
import axios from "axios";

const AutoReplyDashboard = () => {
  const [brand, setBrand] = useState("");
  const [customerMessage, setCustomerMessage] = useState("");
  const [aiReply, setAiReply] = useState("");

  const fetchAutoReply = async () => {
    try {
      const response = await axios.get("http://your-api-url/auto_reply", {
        params: {
          brand: brand,
          message: customerMessage,
        },
      });
      setAiReply(response.data.ai_reply);
    } catch (error) {
      console.error("Error fetching auto-reply:", error);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.header}>🤖 AI Auto-Reply Generator</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Enter Brand Name (e.g., Acme Corp)"
        value={brand}
        onChangeText={setBrand}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter Customer Message"
        value={customerMessage}
        onChangeText={setCustomerMessage}
        multiline
      />
      <Button title="Generate Reply" onPress={fetchAutoReply} />
      
      {aiReply !== "" && (
        <View style={styles.replyContainer}>
          <Text style={styles.subHeader}>AI-Generated Reply:</Text>
          <Text style={styles.replyText}>{aiReply}</Text>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, backgroundColor: "#fff" },
  header: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 10, marginVertical: 10, borderRadius: 5 },
  replyContainer: { marginTop: 20, padding: 10, backgroundColor: "#f9f9f9", borderRadius: 5 },
  subHeader: { fontSize: 18, fontWeight: "bold" },
  replyText: { fontSize: 16, marginTop: 5 },
});

export default AutoReplyDashboard;
