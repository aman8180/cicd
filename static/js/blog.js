// This function runs once the HTML document is fully loaded
document.addEventListener('DOMContentLoaded', (event) => {
  
    // 1. Select the button and code block from the HTML
    const copyButton = document.getElementById('copy-btn');
    const codeBlock = document.getElementById('code-block');
  
    // 2. Only add the click listener if both elements were found
    if (copyButton && codeBlock) {
      
      copyButton.addEventListener('click', () => {
        // 3. Get the text content from the code block
        // .innerText is used to get the text just as it is rendered
        const code = codeBlock.innerText;
  
        // 4. Use the browser's Clipboard API to copy the text
        navigator.clipboard.writeText(code)
          .then(() => {
            // Success! Give user feedback
            copyButton.innerText = 'Copied!';
            copyButton.classList.remove('bg-gray-700', 'hover:bg-gray-600');
            copyButton.classList.add('bg-green-600');
  
            // Reset the button text after 2 seconds
            setTimeout(() => {
              copyButton.innerText = 'Copy';
              copyButton.classList.remove('bg-green-600');
              copyButton.classList.add('bg-gray-700', 'hover:bg-gray-600');
            }, 2000);
          })
          .catch(err => {
            console.error('Failed to copy text: ', err);
            copyButton.innerText = 'Error';
          });
      });
    }
});
