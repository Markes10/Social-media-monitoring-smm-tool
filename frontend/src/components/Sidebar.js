import React, { useContext } from "react";
import { Drawer, List, ListItem, ListItemIcon, ListItemText, IconButton, Switch } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import DescriptionIcon from "@mui/icons-material/Description";
import SettingsIcon from "@mui/icons-material/Settings";
import { ThemeContext } from "../context/ThemeContext";

const Sidebar = ({ open, onClose }) => {
    const { darkMode, setDarkMode } = useContext(ThemeContext);

    return (
        <Drawer anchor="left" open={open} onClose={onClose}>
            <List sx={{ width: 250 }}>
                <ListItem>
                    <ListItemText primary="Navigation" />
                </ListItem>

                <ListItem button onClick={() => (window.location.href = "/dashboard")}>
                    <ListItemIcon>
                        <DashboardIcon />
                    </ListItemIcon>
                    <ListItemText primary="Dashboard" />
                </ListItem>

                <ListItem button onClick={() => (window.location.href = "/reports")}>
                    <ListItemIcon>
                        <DescriptionIcon />
                    </ListItemIcon>
                    <ListItemText primary="Reports" />
                </ListItem>

                <ListItem button onClick={() => (window.location.href = "/settings")}>
                    <ListItemIcon>
                        <SettingsIcon />
                    </ListItemIcon>
                    <ListItemText primary="Settings" />
                </ListItem>

                <ListItem>
                    <ListItemText primary="Dark Mode" />
                    <Switch checked={darkMode} onChange={() => setDarkMode(!darkMode)} />
                </ListItem>
            </List>
        </Drawer>
    );
};

export default Sidebar;
