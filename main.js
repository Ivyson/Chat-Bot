const { exec } = require('child_process');

// Replace 'your-file.cmd' with the actual path to your .cmd file
const cmdFilePath = 'Push.cmd';

exec(cmdFilePath, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error executing ${cmdFilePath}: ${error.message}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});