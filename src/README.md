# Print-piece sources

Rebuild the brochure and agenda from here.

```bash
python3 build.py            # embeds aiims.png / htain.png / qr.png into the .html
node topdf.mjs              # brochure  -> EE-Health-Workshop-Brochure.pdf
node agendapdf.mjs          # agenda    -> EE-Health-Workshop-Agenda.pdf
node meas.mjs               # checks each page still fits 297 mm exactly
```

Edit `brochure.src.html` / `agenda.src.html`, never the built `.html` files —
those have the logos inlined as base64 and are painful to hand-edit.

## Recolouring

Every colour in both documents routes through CSS custom properties in the
`:root` block. To change scheme:

```bash
python3 palettes.py indigo     # current
python3 palettes.py --list     # teal | indigo | maroon | charcoal
python3 build.py && node topdf.mjs && node agendapdf.mjs
```

Adding a scheme is a dozen lines in `palettes.py`.

## Regenerating the QR code

```python
import qrcode
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
q.add_data('https://forms.gle/Te2jRPjubgbfywmm8')
q.make(fit=True)
q.make_image(fill_color='#1c2f5e', back_color='white').save('qr.png')
```

Decode it afterwards to confirm what it actually encodes before printing.

## chk.mjs

The slide overflow checker for the reveal.js decks in the main repository.
Serve the repo root on port 8765, then:

```bash
node chk.mjs block1 block2 block3a block3b block3c
```

Reports slides whose content runs past 700 px of the 720 px slide, em-dash
counts, and any HTTP errors. Run it after every slide edit.
