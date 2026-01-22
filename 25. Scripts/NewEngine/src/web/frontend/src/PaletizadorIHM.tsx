import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Paper, Grid, MenuItem, Select, FormControl, 
  InputLabel, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Button, Divider
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import DashboardIcon from '@mui/icons-material/Dashboard';

const PaletizadorIHM = () => {
  const [ihmType, setIhmType] = useState('siemens');
  const [previewImage, setPreviewImage] = useState('https://via.placeholder.com/400x250?text=IHM+Siemens+Paletizador');

  const handleIhmChange = (event: any) => {
    const value = event.target.value;
    setIhmType(value);
    // Simulação de troca de imagem
    setPreviewImage(`https://via.placeholder.com/400x250?text=IHM+${value.toUpperCase()}+Paletizador`);
  };

  return (
    <Box sx={{ p: 3, backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      {/* "Ribbon" Header Simulado */}
      <Paper elevation={2} sx={{ p: 2, mb: 3, display: 'flex', alignItems: 'center', gap: 2, borderTop: '4px solid #1976d2' }}>
        <DashboardIcon color="primary" fontSize="large" />
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          Configurador de IHM - Paletizador (Módulo Novo)
        </Typography>
        <Box sx={{ flexGrow: 1 }} />
        <Button variant="contained" startIcon={<SaveIcon />}>Salvar Configuração</Button>
      </Paper>

      <Grid container spacing={3}>
        {/* Lado Esquerdo: Seleção e Preview */}
        <Grid item xs={12} md={5}>
          <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>Seleção de IHM</Typography>
            <FormControl fullWidth sx={{ mt: 2, mb: 4 }}>
              <InputLabel>Modelo de Interface</InputLabel>
              <Select value={ihmType} label="Modelo de Interface" onChange={handleIhmChange}>
                <MenuItem value="siemens">Siemens TIA Portal (Novo Padrão)</MenuItem>
                <MenuItem value="zenon">Zenon Copa-Data</MenuItem>
                <MenuItem value="clearline">Clearline KHS Custom</MenuItem>
              </Select>
            </FormControl>

            <Divider sx={{ my: 2 }} />
            
            <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold' }}>Visualização Prévia:</Typography>
            <Box 
              component="img" 
              src={previewImage} 
              sx={{ width: '100%', borderRadius: 2, border: '1px solid #ddd', boxShadow: 'inset 0 0 10px rgba(0,0,0,0.1)' }} 
            />
          </Paper>
        </Grid>

        {/* Lado Direito: Tabela de Dados (Replicando o Excel) */}
        <Grid item xs={12} md={7}>
          <Paper elevation={3} sx={{ p: 0 }}>
            <Box sx={{ p: 2, backgroundColor: '#1976d2', color: 'white', borderTopLeftRadius: 4, borderTopRightRadius: 4 }}>
              <Typography variant="h6">Estrutura de Descritivos (Paletizador)</Typography>
            </Box>
            <TableContainer>
              <Table size="small">
                <TableHead sx={{ backgroundColor: '#eee' }}>
                  <TableRow>
                    <TableCell><b>Seção</b></TableCell>
                    <TableCell><b>Descrição Técnica</b></TableCell>
                    <TableCell align="center"><b>Aplicável?</b></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {[
                    { sec: '1.0', desc: 'Interface de Operação Principal', app: 'Sim' },
                    { sec: '1.1', desc: 'Status de Mensagens e Alarmes', app: 'Sim' },
                    { sec: '2.0', desc: 'Controle de Produção e Cadência', app: 'Sim' },
                    { sec: '3.0', desc: 'Diagnóstico de Falhas em Motores', app: 'Sim' },
                    { sec: '4.0', desc: 'Configuração de Camadas (Paletização)', app: 'Sim' },
                    { sec: '5.0', desc: 'Parada de Emergência e Segurança', app: 'Sim' },
                  ].map((row, idx) => (
                    <TableRow key={idx} hover>
                      <TableCell>{row.sec}</TableCell>
                      <TableCell>{row.desc}</TableCell>
                      <TableCell align="center">{row.app}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PaletizadorIHM;
