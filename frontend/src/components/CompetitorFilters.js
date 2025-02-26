import React, { useState } from "react";
import { Box, MenuItem, Select, Button, TextField } from "@mui/material";

const CompetitorFilters = ({ onFilterChange }) => {
    const [brands, setBrands] = useState([]);
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const handleFilter = () => {
        onFilterChange({ brands, startDate, endDate });
    };

    return (
        <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
            <Select
                multiple
                value={brands}
                onChange={(e) => setBrands(e.target.value)}
                displayEmpty
                sx={{ minWidth: 200 }}
            >
                <MenuItem value="BrandA">Brand A</MenuItem>
                <MenuItem value="BrandB">Brand B</MenuItem>
                <MenuItem value="BrandC">Brand C</MenuItem>
            </Select>

            <TextField
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
            />
            <TextField
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
            />

            <Button variant="contained" onClick={handleFilter}>
                Apply Filters
            </Button>
        </Box>
    );
};

export default CompetitorFilters;
