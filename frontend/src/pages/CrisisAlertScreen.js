import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const CrisisAlertScreen = () => {
    const [brand, setBrand] = useState("");
    const [platform, setPlatform] = useState("Twitter");
    const [alert, setAlert] = useState(null);

    const checkCrisis = async () => {
        const response = await axios.get(`http://your-api-url/crisis-detection?brand=${brand}&platform=${platform}`);
        setAlert(response.data.crisis_alert);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🚨 Crisis Detection</Text>
            <TextInput style={styles.input} placeholder="Enter Brand Name" value={brand} onChangeText={setBrand} />
            <Button title="Check Crisis Alert" onPress={checkCrisis} />
            {alert && (
                <Text>🔥 Crisis Alert: {alert.crisis_alert ? "Yes, take action!" : "No major issues."}</Text>
            )}
        </View>
    );
};

export default CrisisAlertScreen;
