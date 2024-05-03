tinyMCE.init({
        selector: ".tiny-class",
        editor_selector : ".tiny-class",
        height: 600,
        relative_urls : false,
        remove_script_host : false,
        plugins: [
          'autolink lists link image code',
          'media table paste wordcount',
          'visualblocks preview anchor'
        ],
        menubar: false,
        image_caption: true,
        toolbar: 'undo redo | styleselect | blockquote | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist | link image media | indent outdent | visualblocks | code',
        formats: {
          informationFormat: {
            block: 'div', classes: 'information'
          }
        },
        style_formats: [
          { title: 'Headings', items: [
            {title: 'Headings 2', format: 'h2'},
            {title: 'Headings 3', format: 'h3'},
            {title: 'Headings 4', format: 'h4'},
            {title: 'Headings 5', format: 'h5'},
            {title: 'Headings 6', format: 'h6'}
          ]},
          {title: 'Inline', items: [
            {title: 'Bold', format: 'bold'},
            {title: 'Italic', format: 'italic'},
            {title: 'Underline', format: 'underline'},
            {title: 'Strikethrough', format: 'strikethrough'},
          ]},
          {title: 'Blocks', items: [
            {title: 'Paragraph', format: 'p'},
            {title: 'Blockquote', format: 'blockquote'},
            {title: 'Information', format: 'informationFormat'},
          ]},
          {title: 'Alignment', items: [
            {title: 'Left', format: 'alignleft'},
            {title: 'Center', format: 'aligncenter'},
            {title: 'Right', format: 'alignright'},
            {title: 'Justify', format: 'alignjustify'}
          ]}
        ],
        forced_root_block : false,
        default_font_stack: [ '-apple-system', 'Helvetica', 'Arial', 'sans-serif' ],
        content_style: `
        h1,h2,h3 {
          clear:both;
        }
        .align-left {
          float: left;
          margin-right: 1rem;
          margin-bottom: 1rem;
        }
        .align-right {
          float: right;
          margin-left: 1rem;
          margin-bottom: 1rem;
        }
        .information {
           clear: both;
           padding: 1rem;
           background: lightgray;
        }`
      });
