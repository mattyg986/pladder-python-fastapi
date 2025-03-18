import React from 'react';
import { useQuery } from 'react-query';
import { 
  Box, 
  Card, 
  CardContent, 
  Typography, 
  Grid, 
  Paper, 
  Container,
  CircularProgress
} from '@mui/material';
import { 
  SmartToy as AgentsIcon,
  Task as TasksIcon,
  Check as CompletedIcon,
  Error as ErrorIcon 
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

import { fetchAgents, fetchTasks } from '../services/api';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StatCard = ({ title, value, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Grid container spacing={2} alignItems="center">
        <Grid item>
          <Box 
            sx={{ 
              backgroundColor: `${color}.light`, 
              borderRadius: '50%', 
              display: 'flex', 
              padding: 1
            }}
          >
            {icon}
          </Box>
        </Grid>
        <Grid item xs>
          <Typography variant="h6" component="div" color="text.secondary">
            {title}
          </Typography>
          <Typography variant="h4" component="div">
            {value}
          </Typography>
        </Grid>
      </Grid>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const { data: agents, isLoading: isLoadingAgents } = useQuery('agents', fetchAgents);
  const { data: tasks, isLoading: isLoadingTasks } = useQuery('tasks', fetchTasks);

  // Simulated chart data
  const chartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'Tasks Processed',
        data: [65, 59, 80, 81, 56, 55, 40],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: 'Success Rate',
        data: [28, 48, 40, 19, 86, 27, 90],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Agent Activity',
      },
    },
  };

  if (isLoadingAgents || isLoadingTasks) {
    return <CircularProgress />;
  }

  // Mock data for now
  const agentCount = agents?.length || 0;
  const taskCount = tasks?.length || 0;
  const completedTasks = tasks?.filter(task => task.status === 'completed').length || 0;
  const failedTasks = tasks?.filter(task => task.status === 'failed').length || 0;

  return (
    <Container maxWidth="xl">
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Total Agents" 
            value={agentCount} 
            icon={<AgentsIcon color="primary" />} 
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Total Tasks" 
            value={taskCount} 
            icon={<TasksIcon color="secondary" />} 
            color="secondary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Completed Tasks" 
            value={completedTasks} 
            icon={<CompletedIcon color="success" />} 
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Failed Tasks" 
            value={failedTasks} 
            icon={<ErrorIcon color="error" />} 
            color="error"
          />
        </Grid>
      </Grid>
      
      <Box mt={4}>
        <Paper sx={{ p: 3 }}>
          <Line options={options} data={chartData} />
        </Paper>
      </Box>
    </Container>
  );
};

export default Dashboard; 