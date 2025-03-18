import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  CircularProgress,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
  Stack,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

import { fetchAgent, fetchAgentTasks, createAgentTask } from '../services/api';

const getStatusColor = (status) => {
  switch (status) {
    case 'active':
    case 'completed':
      return 'success';
    case 'paused':
    case 'running':
      return 'warning';
    case 'stopped':
    case 'failed':
      return 'error';
    case 'queued':
      return 'info';
    default:
      return 'default';
  }
};

const TaskDialog = ({ open, handleClose, handleSubmit, agentType }) => {
  const [taskData, setTaskData] = useState({
    action: '',
    parameters: {},
    priority: 0,
  });

  const [parametersText, setParametersText] = useState('{}');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTaskData({ ...taskData, [name]: value });
  };

  const handleParametersChange = (e) => {
    setParametersText(e.target.value);
    try {
      const parameters = JSON.parse(e.target.value);
      setTaskData({ ...taskData, parameters });
    } catch (error) {
      // Invalid JSON, we'll handle validation on submit
    }
  };

  const onSubmit = () => {
    try {
      const parameters = JSON.parse(parametersText);
      const data = { ...taskData, parameters };
      handleSubmit(data);
      setTaskData({
        action: '',
        parameters: {},
        priority: 0,
      });
      setParametersText('{}');
    } catch (error) {
      alert('Invalid JSON in parameters field');
    }
  };

  const getSuggestedActions = () => {
    switch (agentType) {
      case 'recruiter':
        return ['process_candidate', 'search_candidates'];
      case 'processor':
        return ['process_application', 'evaluate_application'];
      case 'matcher':
        return ['match_candidates', 'score_candidate'];
      case 'search':
        return ['search_jobs', 'search_candidates'];
      default:
        return [];
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Create New Task</DialogTitle>
      <DialogContent>
        <Box component="form" sx={{ mt: 2 }}>
          <TextField
            fullWidth
            margin="normal"
            name="action"
            label="Task Action"
            helperText={`Suggested actions: ${getSuggestedActions().join(', ')}`}
            value={taskData.action}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            margin="normal"
            name="priority"
            label="Priority"
            type="number"
            value={taskData.priority}
            onChange={handleChange}
            helperText="Higher number = higher priority"
          />
          <TextField
            fullWidth
            margin="normal"
            name="parameters"
            label="Parameters (JSON)"
            value={parametersText}
            onChange={handleParametersChange}
            multiline
            rows={6}
            error={parametersText !== '{}' && !isValidJson(parametersText)}
            helperText={
              parametersText !== '{}' && !isValidJson(parametersText)
                ? 'Invalid JSON'
                : 'Enter parameters in JSON format'
            }
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button
          onClick={onSubmit}
          variant="contained"
          color="primary"
          disabled={
            !taskData.action ||
            (parametersText !== '{}' && !isValidJson(parametersText))
          }
        >
          Create Task
        </Button>
      </DialogActions>
    </Dialog>
  );
};

function isValidJson(str) {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}

const AgentDetail = () => {
  const { agentId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [taskDialogOpen, setTaskDialogOpen] = useState(false);

  const {
    data: agent,
    isLoading: isLoadingAgent,
    error: agentError,
  } = useQuery(['agent', agentId], () => fetchAgent(agentId), {
    enabled: !!agentId,
  });

  const { data: tasks, isLoading: isLoadingTasks } = useQuery(
    ['agentTasks', agentId],
    () => fetchAgentTasks(agentId),
    {
      enabled: !!agentId,
    }
  );

  const createTaskMutation = useMutation(
    (taskData) => createAgentTask(agentId, taskData),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['agentTasks', agentId]);
        setTaskDialogOpen(false);
      },
    }
  );

  const handleTaskDialogOpen = () => {
    setTaskDialogOpen(true);
  };

  const handleTaskDialogClose = () => {
    setTaskDialogOpen(false);
  };

  const handleCreateTask = (taskData) => {
    createTaskMutation.mutate(taskData);
  };

  if (isLoadingAgent) {
    return <CircularProgress />;
  }

  if (agentError) {
    return (
      <Container>
        <Typography variant="h5" color="error">
          Error loading agent: {agentError.message}
        </Typography>
        <Button variant="contained" onClick={() => navigate('/agents')}>
          Back to Agents
        </Button>
      </Container>
    );
  }

  if (!agent) {
    return (
      <Container>
        <Typography variant="h5">Agent not found</Typography>
        <Button variant="contained" onClick={() => navigate('/agents')}>
          Back to Agents
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box mb={4}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h4">Agent Details</Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={handleTaskDialogOpen}
          >
            Create Task
          </Button>
        </Stack>

        <Paper sx={{ p: 3, mb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                {agent.name}
              </Typography>
              <Chip
                label={agent.type}
                color="primary"
                sx={{ mr: 1 }}
              />
              <Chip
                label={agent.status}
                color={getStatusColor(agent.status)}
              />
              <Typography variant="body1" sx={{ mt: 2 }}>
                {agent.description || 'No description provided'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Parameters
              </Typography>
              <Box
                component="pre"
                sx={{
                  backgroundColor: 'rgba(0, 0, 0, 0.04)',
                  p: 2,
                  borderRadius: 1,
                  overflow: 'auto',
                  maxHeight: '200px',
                }}
              >
                {JSON.stringify(agent.parameters, null, 2)}
              </Box>
            </Grid>
          </Grid>
        </Paper>

        <Typography variant="h5" gutterBottom>
          Tasks
        </Typography>
        {isLoadingTasks ? (
          <CircularProgress />
        ) : (
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="tasks table">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Action</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created At</TableCell>
                  <TableCell>Completed At</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tasks && tasks.length > 0 ? (
                  tasks.map((task) => (
                    <TableRow key={task.task_id} hover>
                      <TableCell>{task.task_id}</TableCell>
                      <TableCell>{task.action}</TableCell>
                      <TableCell>
                        <Chip
                          label={task.status}
                          color={getStatusColor(task.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {task.created_at
                          ? new Date(task.created_at).toLocaleString()
                          : 'N/A'}
                      </TableCell>
                      <TableCell>
                        {task.completed_at
                          ? new Date(task.completed_at).toLocaleString()
                          : 'N/A'}
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      No tasks found for this agent.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Box>

      <TaskDialog
        open={taskDialogOpen}
        handleClose={handleTaskDialogClose}
        handleSubmit={handleCreateTask}
        agentType={agent.type}
      />
    </Container>
  );
};

export default AgentDetail; 