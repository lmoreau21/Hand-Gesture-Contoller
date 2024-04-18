import React, { useState, useEffect } from 'react';
import { Snackbar, Alert, CssBaseline, Box, Button, TextField, Typography, MenuItem, Select, FormControl, InputLabel, Table, TableBody, TableCell, TableRow, TableContainer, Paper, useMediaQuery, createTheme, ThemeProvider, Switch, FormGroup, FormControlLabel, Container, Stack, TableHead } from '@mui/material';
import axios from 'axios';

function App() {
  const [alert, setAlert] = useState({
    open: false,
    message: '',
    type: 'success',
    duration: 6000 
  });
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const [mode, setMode] = useState(prefersDarkMode ? 'dark' : 'light');
  const [folders, setFolders] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState('');
  const [keybinds, setKeybinds] = useState({ '': ''});
  const [newFolderName, setNewFolderName] = useState('');
  const [testInput, setTestInput] = useState('');
  const [newGesture, setNewGesture] = useState('');
  const [newKey, setNewKey] = useState('');
  const KEYBOARD_MAPPING_KEYS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'space', 'up', 'left', 'down', 'right',
    'escape', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'scrolllock', 'pause', '`', '-', '=', 'backspace', 'insert', 'home', 'pageup', 'pagedown',
    'numlock', 'divide', 'multiply', 'subtract', 'add', 'decimal', 'numpadenter', 'numpad1', 'numpad2',
    'numpad3', 'numpad4', 'numpad5', 'numpad6', 'numpad7', 'numpad8', 'numpad9', 'numpad0', 'tab', '[', ']', '\\', 'del', 'delete', 'end', 'capslock',
    ';', "'", 'enter', 'return', 'shift', 'shiftleft', ',', '.', '/', 'shiftright', 'ctrl', 'ctrlleft', 'win', 'winleft', 'alt', 'altleft',
    'altright', 'winright', 'apps', 'ctrlright'
  ];
  const theme = createTheme({
    palette: {
      mode: mode,
    }    
  });

  const toggleDarkMode = () => {
    setMode(prevMode => (prevMode === 'light' ? 'dark' : 'light'));
  };

  function showAlert(message, type = 'success', duration = 6000) {
    setAlert({ open: true, message, type });
  }

  
  useEffect(() => {
    const getFolders = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get_folder_list');
        setFolders(response.data);
        if (response.data.length > 0 && !selectedFolder) {
          setSelectedFolder(response.data[0]);
        }
      } catch (error) {
        console.error('Error fetching folders', error);
      }
    };

    getFolders();
  }, []);

  // Fetch folder list from the server
  function fetchFolders() {
    return fetch("http://127.0.0.1:5000/get_folder_list")
      .then(res => res.json())
      .then(data => {
        setFolders(data);
        if (data.length > 0 && !selectedFolder) {
          setSelectedFolder(data[0]);
        }
      })
      .catch(err => console.error("Error fetching folders:", err));
  }

  // Handle creating a new folder
  function handleCreateFolder() {
    fetch('http://127.0.0.1:5000/create_folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder_name: newFolderName })
    })
    .then(data => {
      console.log('Folder created:', data);
      fetchFolders().then(() => {
        setSelectedFolder(newFolderName);
        setNewFolderName('');
      });
    })
    .catch(error => {
      console.error('Error creating folder:', error)
      showAlert('Failed to creating folder.', 'error');
    });
    
  }

  // Fetch keybinds for a selected folder
  useEffect(() => {
    if (selectedFolder) {
      fetchKeybinds(selectedFolder);
    }
  }, [selectedFolder]);

  function fetchKeybinds(folder) {
    fetch(`http://127.0.0.1:5000/get_dicts?folder=${selectedFolder}`)
      .then(res => res.json())
      .then(data => {
        setKeybinds(data);
      })
      .catch(err => showAlert("Error fetching keybinds. Reload Page", 'error'));
  }

  function addKeybindRow() {
    setKeybinds(prev => ({ ...prev, [newGesture]: newKey }));
    setNewGesture('');
    setNewKey('');
    
  }

  function updateKeybind(oldGesture, newGesture, newKey) {
    if (newGesture !== oldGesture) {
      setKeybinds(prev => {
        const { [oldGesture]: _, ...rest } = prev;
        return { ...rest, [newGesture]: newKey };
      });
    } else {
      setKeybinds(prev => ({ ...prev, [newGesture]: newKey }));
    }
  }

  function removeKeybind(gesture) {
    setKeybinds(prev => {
      const { [gesture]: _, ...rest } = prev;
      return rest;
    });
  }
  

  function saveKeybinds() {
    fetch('http://127.0.0.1:5000/update_dicts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keybinds_dict: keybinds, folder_name: selectedFolder})
    })
    .then(() => showAlert('Keybinds saved successfully!', 'success'))
    .catch(error => {
      console.error('Error saving keybinds:', error)
      showAlert('Failed to save keybinds.', 'error');
    });
  }

  function handleCreateImages() {
    fetch('http://127.0.0.1:5000/create_images', { 
      method: 'POST' ,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder_name: selectedFolder, keybinds_dict: keybinds })
    })
      .then(() => showAlert('Images created successfully!', 'success'))
      .catch(err => showAlert('Error has occured. try again later', 'error'));
  }

  function runClassifier() {
    fetch('http://127.0.0.1:5000/inference_classifier', { 
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder_name: selectedFolder, keybinds_dict: keybinds })
      })
      .then(() => console.log('Classifier ran successfully!'))
      .catch(err => showAlert('Failed to run classifier', 'error'));
  }
  
  return (
    <ThemeProvider theme={theme}>
       <CssBaseline />
       <Container sx={{ bgcolor: 'background.default', height: '100vh',  width:'100vw' }}>
      <Box sx={{ padding: 4 }}>
      
      <Stack direction={'row'} justifyContent="space-between">
      <Typography variant="h5" gutterBottom>Hand Symbol Keybind</Typography>
      <FormGroup>
          <FormControlLabel control={<Switch checked={mode === 'dark'} onChange={toggleDarkMode} />} label={mode+' mode'} />
        </FormGroup>
      </Stack>
      <Typography paragraph>Follow the steps below to create a keybind, record images, train the model, and run the classifier.</Typography>
      <Stack  spacing={2}>
        <Box>
      <Typography variant="subtitle1">Step 1: Name your keybind and or select keybind from dropdown</Typography>
      <Stack direction={'row'} justifyContent="flex-start" alignItems="center" spacing={2}>
        <TextField
          label="Folder Name"
          value={newFolderName}
          onChange={(e) => setNewFolderName(e.target.value)}
          margin="normal"
          variant="standard"
        />
        <Button onClick={handleCreateFolder} variant="outlined">Create Folder</Button>
      </Stack> 
       
      <FormControl fullWidth margin="normal">
        <InputLabel id="select-keybind-label">Select Keybind Name</InputLabel>
        <Select
          labelId="select-keybind-label"
          value={selectedFolder}
          variant="filled"
          onChange={(e) => setSelectedFolder(e.target.value)}
        >
          {folders.map(folder => <MenuItem key={folder} value={folder}>{folder}</MenuItem>)}
        </Select>
      </FormControl>
      </Box>
      <Box>
      <Typography variant="subtitle1">Step 2: Create Images: Records 100 frames of you performing the gesture. Then, it trains the model. Make sure the frame is selected when you press 'Q'</Typography>
      <Button variant="outlined" onClick={handleCreateImages}>Create Images</Button>
      </Box>
      <Box>
      <Typography variant="subtitle1">Step 3: Run Classifier: Tracks hand and presses keys. Press 'q' to quit popup when it is selected</Typography>
      <Button variant="outlined" onClick={runClassifier}>Run Classifier</Button>
      </Box>
      <Box>

      <Typography variant="h6">Keybinds: {selectedFolder}</Typography>
      
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Gesture Name</TableCell>
              <TableCell>Key</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.entries(keybinds).map(([gesture, key], index) => (
              <TableRow>
                <TableCell>
                  <TextField
                    value={gesture}
                    variant="standard"
                    onChange={e => updateKeybind(gesture, e.target.value, key)}
                    fullWidth
                  />
                </TableCell>
                <TableCell>
                  <FormControl fullWidth>
                    <Select
                      variant="standard"
                      value={key}
                      onChange={e => updateKeybind(gesture, gesture, e.target.value)}
                      displayEmpty
                    >
                   {KEYBOARD_MAPPING_KEYS.map((keyOption) => (
                    <MenuItem value={keyOption}>{keyOption}</MenuItem >
              ))}
              </Select>
            </FormControl>
          </TableCell>
          <TableCell>
            <Button onClick={() => removeKeybind(gesture)} variant="outlined" color="error">Remove</Button>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
  </TableContainer>
  </Box>
    <Stack direction={'row'} spacing={2} >
      <Button onClick={addKeybindRow} variant="outlined">Add Row</Button>
      <Button onClick={saveKeybinds} variant="outlined">Save Changes</Button>
    </Stack>
  </Stack>
  </Box>
  <Snackbar
  open={alert.open}
  autoHideDuration={alert.duration}
  onClose={() => setAlert({ ...alert, open: false })}
  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}  // This positions the Snackbar at the bottom right
>
  <Alert 
    onClose={() => setAlert({ ...alert, open: false })} 
    severity={alert.type} 
    variant="outlined"  
  >
    {alert.message}
  </Alert>
</Snackbar>
  </Container>
  </ThemeProvider>
  );
}

export default App;