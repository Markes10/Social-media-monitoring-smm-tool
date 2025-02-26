import React, { useEffect, useState } from "react";
import { fetchPosts } from "../api";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { Box, Typography } from "@mui/material";

const COLORS = ["#4CAF50", "#F44336", "#FFC107"]; // Green, Red, Yellow

const SentimentChart = () => {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetchPosts().then(posts => {
            const sentimentCounts = { Positive: 0, Negative: 0, Neutral: 0 };
            posts.forEach(post => sentimentCounts[post.sentiment]++);

            setChartData([
                { name: "Positive", value: sentimentCounts.Positive },
                { name: "Negative", value: sentimentCounts.Negative },
                { name: "Neutral", value: sentimentCounts.Neutral }
            ]);
        });
    }, []);

    return (
        <Box sx={{ textAlign: "center", mt: 3 }}>
            <Typography variant="h6">Sentiment Analysis</Typography>
            <PieChart width={300} height={300}>
                <Pie data={chartData} dataKey="value" outerRadius={100} fill="#8884d8">
                    {chartData.map((entry, index) => (
                        <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip />
                <Legend />
            </PieChart>
        </Box>
    );
};

export default SentimentChart;
