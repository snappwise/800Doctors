// document.addEventListener('DOMContentLoaded', function() {
//     const fileInputs = document.querySelectorAll('.inline-related:not(.empty-form) input[type="file"]');
    
//     fileInputs.forEach(input => {
//         // Enable multiple file selection
//         input.setAttribute('multiple', 'multiple');
        
//         input.addEventListener('change', function(e) {
//             const files = e.target.files;
//             const inlineGroup = this.closest('.inline-group');
//             const totalFormsInput = inlineGroup.querySelector('[name$="-TOTAL_FORMS"]');
            
//             if (!files.length) return;

//             // Update display to show selected files
//             let fileInfoDiv = this.parentNode.querySelector('.selected-files-info');
//             if (!fileInfoDiv) {
//                 fileInfoDiv = document.createElement('div');
//                 fileInfoDiv.className = 'selected-files-info';
//                 this.parentNode.appendChild(fileInfoDiv);
//             }

//             let filesList = '';
//             for (let i = 0; i < files.length; i++) {
//                 const file = files[i];
//                 const size = (file.size / 1024).toFixed(1);
//                 filesList += `<div>${file.name} (${size} KB)</div>`;
//             }
//             fileInfoDiv.innerHTML = `<strong>Selected ${files.length} files:</strong><br>${filesList}`;

//             // Update the total forms count to match the number of files
//             totalFormsInput.value = files.length;
            
//             // Update management form data
//             const maxFormsInput = inlineGroup.querySelector('[name$="-MAX_NUM_FORMS"]');
//             if (maxFormsInput && maxFormsInput.value !== '') {
//                 const maxForms = parseInt(maxFormsInput.value);
//                 if (maxForms > 0 && files.length > maxForms) {
//                     alert(`You can only upload up to ${maxForms} files.`);
//                     this.value = '';
//                     return;
//                 }
//             }
//         });
//     });
// });


document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('.inline-related:not(.empty-form) input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0]; // Get the first (and only) file
            const inlineGroup = this.closest('.inline-group');
            const totalFormsInput = inlineGroup.querySelector('[name$="-TOTAL_FORMS"]');
            
            if (!file) return;

            // Update display to show selected file
            let fileInfoDiv = this.parentNode.querySelector('.selected-files-info');
            if (!fileInfoDiv) {
                fileInfoDiv = document.createElement('div');
                fileInfoDiv.className = 'selected-files-info';
                this.parentNode.appendChild(fileInfoDiv);
            }

            const size = (file.size / 1024).toFixed(1); // File size in KB
            fileInfoDiv.innerHTML = `<strong>Selected file:</strong><br>${file.name} (${size} KB)`;

            // Update the total forms count to match the number of files (1 file)
            totalFormsInput.value = 1;
            
            // Update management form data
            const maxFormsInput = inlineGroup.querySelector('[name$="-MAX_NUM_FORMS"]');
            if (maxFormsInput && maxFormsInput.value !== '') {
                const maxForms = parseInt(maxFormsInput.value);
                if (maxForms > 0 && 1 > maxForms) { // This check might not be necessary since we're allowing only 1 file
                    alert(`You can only upload up to ${maxForms} file.`);
                    this.value = ''; // Reset the input
                    return;
                }
            }
        });
    });
});
