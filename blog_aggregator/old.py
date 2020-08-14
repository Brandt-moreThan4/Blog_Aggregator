def make_word_doc():
    """Make a word doc from the post objects"""
    
    doc = Document()
    for post in all_posts:
        doc.add_paragraph('\n\n----NEW POSTTTTT---\n\n')
        doc.add_paragraph(post.title + '\n')
        doc.add_paragraph(str(post.date) + '\n')
        chunks  = []
        for typey, content in post.body:
            if typey == 'image':
                doc.add_paragraph(''.join(chunks))
                chunks = []
                doc.add_picture(content, width=Inches(6.5))
            else:
                chunks.append(content)
        if chunks:
            doc.add_paragraph(''.join(chunks))
        
        doc.add_paragraph('\n\n-------END POST------\n\n\n\n\n\n')
    
    doc.save('aswath.docx')



def make_html():

    with (Path.cwd() / 'test_aswath') as f:
        for post in all_posts:
            # filtered = [x[1] for x in post.body]
            f.write('<div>----NEW POSTTTTT---</div>')
            f.write(f'<div>----{post.title}---</div>')
            f.write(f'<div>----{post.date}---</div>')
            
            chunks  = []
            for typey, content in post.body:
                if typey == 'image':
                    f.write(f"<pre>{''.join(chunks)}</pre>")
                    chunks = []
                    f.write(f'<img src="{content}"></img>')
                else:
                    chunks.append(content)
            if chunks:
                f.write(f"<pre>{''.join(chunks)}</pre>")
            f.write(f"<div>-------END POST------</div>")