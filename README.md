# christinedekock.com

Personal site for Christine de Kock. Plain static HTML and CSS — no theme, no
framework, no build step. GitHub Pages serves the files as-is (`.nojekyll`).

    index.html            the whole site; edit this to add a paper or student
    style.css             all styling; light and dark palettes via CSS variables
    404.html              not-found page
    publications/         redirect stub, kept so old /publications links resolve
    assets/img/           banner.jpg and portrait.jpg are the two images in use;
                          the IMG_*.jpg files are the full-size originals
    christine_cv.pdf      linked from the header

To add a publication, copy an existing `<li>` in the `ol.papers` list and edit
the three parts: `<span class="meta">` (authors and year), the `<a class="title">`
(title and link), and `<span class="venue">` (venue).

Images are resized before committing, e.g.
`sips -s format jpeg -s formatOptions 82 --resampleWidth 2000 in.jpg --out out.jpg`
