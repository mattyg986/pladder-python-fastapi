import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Link } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Stack,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

import { fetchAgents, createAgent } from '../services/api';

const getStatusColor = (status) => {
  switch (status) {
    case 'active':
      return 'success';
    case 'paused':
      return 'warning';
    case 'stopped':
      return 'error';
    case 'error':
      return 'error';
    default:
      return 'default';
  }
};

const AgentDialog = ({ open, handleClose, handleSubmit }) => {
  const [agentData, setAgentData] = useState({
    name: '',
    type: '',
    description: '',
    parameters: {},
  });
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setAgentData({ ...agentData, [name]: value });
  };
  
  const onSubmit = () => {
    handleSubmit(agentData);
    setAgentData({
      name: '',
      type: '',
      description: '',
      parameters: {},
    });
  };
  
  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create New Agent</DialogTitle>
      <DialogContent>
        <Box component="form" sx={{ mt: 2 }}>
          <TextField
            fullWidth
            margin="normal"
            name="name"
            label="Agent Name"
            value={agentData.name}
            onChange={handleChange}
            required
          />
          <FormControl fullWidth margin="normal" required>
            <InputLabel id="agent-type-label">Agent Type</InputLabel>
            <Select
              labelId="agent-type-label"
              name="type"
              value={agentData.type}
              onChange={handleChange}
              label="Agent Type"
            >
              <MenuItem value="recruiter">Recruiter</MenuItem>
              <MenuItem value="processor">Processor</MenuItem>
              <MenuItem value="matcher">Matcher</MenuItem>
              <MenuItem value="search">Search</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            margin="normal"
            name="description"
            label="Description"
            value={agentData.description}
            onChange={handleChange}
            multiline
            rows={3}
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={onSubmit} variant="contained" color="primary">
          Create
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const Agents = () => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const queryClient = useQueryClient();
  
  const { data: agents, isLoading } = useQuery('agents', fetchAgents);
  
  const createAgentMutation = useMutation(createAgent, {
    onSuccess: () => {
      queryClient.invalidateQueries('agents');
      setDialogOpen(false);
    },
  });
  
  const handleDialogOpen = () => {
    setDialogOpen(true);
  };
  
  const handleDialogClose = () => {
    setDialogOpen(false);
  };
  
  const handleCreateAgent = (agentData) => {
    createAgentMutation.mutate(agentData);
  };

  if (isLoading) {
    return <CircularProgress />;
  }

  return (
    <Container maxWidth="xl">
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Agents</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleDialogOpen}
        >
          Create Agent
        </Button>
      </Stack>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="agents table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {agents && agents.length > 0 ? (
              agents.map((agent) => (
                <TableRow key={agent.id} hover component={Link} to={`/agents/${agent.id}`} sx={{ textDecoration: 'none' }}>
                  <TableCell component="th" scope="row">
                    {agent.name}
                  </TableCell>
                  <TableCell>{agent.type}</TableCell>
                  <TableCell>{agent.description}</TableCell>
                  <TableCell>
                    <Chip
                      label={agent.status}
                      color={getStatusColor(agent.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(agent.created_at).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  No agents found. Create your first agent to get started.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <AgentDialog
        open={dialogOpen}
        handleClose={handleDialogClose}
        handleSubmit={handleCreateAgent}
      />
    </Container>
  );
};

export default Agents; 