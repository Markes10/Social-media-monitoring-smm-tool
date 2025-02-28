import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import messaging from "@react-native-firebase/messaging";
import axios from "axios";
import Dashboard from "./pages/Dashboard";
import ThemeProviderWrapper from "./context/ThemeContext";
import { CssBaseline } from "@mui/material";

const App = () => {
    const [trends, setTrends] = useState([]);

    useEffect(() => {
        const setupNotifications = async () => {
            const authStatus = await messaging().requestPermission();
            const enabled = authStatus === messaging.AuthorizationStatus.AUTHORIZED || authStatus === messaging.AuthorizationStatus.PROVISIONAL;
            
            if (enabled) {
                console.log("Notification permission granted.");
                await messaging().subscribeToTopic("alerts");
                console.log("Subscribed to alerts!");
            }
        };

        setupNotifications();
        axios.get("http://your-ec2-ip:8000/sentiment-trends?days=7")
            .then(response => setTrends(Object.entries(response.data).map(([date, values]) => ({ date, ...values }))))
            .catch(error => console.error("Error fetching trends:", error));
    }, []);

    return (
        <ThemeProviderWrapper>
            <CssBaseline />
            <Router>
                <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
            </Router>
            <View style={styles.container}>
                <Text style={styles.header}>Sentiment Trends</Text>
                <FlatList
                    data={trends}
                    keyExtractor={(item) => item.date}
                    renderItem={({ item }) => (
                        <View style={styles.item}>
                            <Text>Date: {item.date}</Text>
                            <Text>Positive: {item.positive}</Text>
                            <Text>Negative: {item.negative}</Text>
                            <Text>Neutral: {item.neutral}</Text>
                        </View>
                    )}
                />
            </View>
        </ThemeProviderWrapper>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20, backgroundColor: "#fff" },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    item: { padding: 10, borderBottomWidth: 1, borderBottomColor: "#ddd" },
});

export default App;
