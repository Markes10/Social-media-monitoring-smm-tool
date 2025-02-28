import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, ScrollView } from "react-native";
import axios from "axios";

const CompetitorInsights = () => {
  const [competitor, setCompetitor] = useState("");
  const [insights, setInsights] = useState("");

  const fetchInsights = async () => {
    try {
      const response = await axios.get("http://your-api-url/competitor_insights", {
        params: { competitor },
      });
      setInsights(response.data.ai_insights);
    } catch (error) {
      console.error("Error fetching insights:", error);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.header}>📊 Competitor Insights</Text>

      <TextInput
        style={styles.input}
        placeholder="Enter Competitor (e.g., Nike)"
        value={competitor}
        onChangeText={setCompetitor}
      />
      <Button title="Get Insights" onPress={fetchInsights} />

      {insights !== "" && (
        <View style={styles.insightsContainer}>
          <Text style={styles.subHeader}>AI-Generated Insights:</Text>
          <Text style={styles.insightsText}>{insights}</Text>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, backgroundColor: "#fff" },
  header: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 10, marginVertical: 10, borderRadius: 5 },
  insightsContainer: { marginTop: 20, padding: 10, backgroundColor: "#f9f9f9", borderRadius: 5 },
  subHeader: { fontSize: 18, fontWeight: "bold" },
  insightsText: { fontSize: 16, marginTop: 5 },
});

export default CompetitorInsights;

