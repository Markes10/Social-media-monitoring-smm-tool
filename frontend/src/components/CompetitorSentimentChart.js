import React, { useEffect, useState } from "react";
import { fetchCompetitorData } from "../api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Box, Typography } from "@mui/material";
import CompetitorFilters from "./CompetitorFilters";

const CompetitorSentimentChart = () => {
    const [chartData, setChartData] = useState([]);

    const loadCompetitorData = (filters) => {
        fetchCompetitorData(filters.brands, filters.startDate, filters.endDate).then(posts => {
            const sentimentCounts = {};

            posts.forEach(post => {
                const key = post.brand;
                if (!sentimentCounts[key]) {
                    sentimentCounts[key] = { brand: key, Positive: 0, Negative: 0, Neutral: 0 };
                }
                sentimentCounts[key][post.sentiment]++;
            });

            setChartData(Object.values(sentimentCounts));
        });
    };

    useEffect(() => {
        loadCompetitorData({ brands: ["BrandA", "BrandB"] });
    }, []);

    return (
        <Box sx={{ textAlign: "center", mt: 3 }}>
            <Typography variant="h6">Competitor Sentiment Analysis</Typography>
            <CompetitorFilters onFilterChange={loadCompetitorData} />
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                    <XAxis dataKey="brand" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="Positive" fill="#4CAF50" />
                    <Bar dataKey="Negative" fill="#F44336" />
                    <Bar dataKey="Neutral" fill="#FFC107" />
                </BarChart>
            </ResponsiveContainer>
        </Box>
    );
};

export default CompetitorSentimentChart;
