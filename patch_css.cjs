const fs = require('fs');
let css = fs.readFileSync('style.css', 'utf-8');

const replacement = \details.step-card {
  /* Inherits from .step-card */
}
details.step-card summary {
  cursor: pointer;
  user-select: none;
  list-style: none;
  outline: none;
}
details.step-card summary::-webkit-details-marker {
  display: none;
}
details.step-card summary::after {
  content: "▼";
  display: inline-block;
  float: right;
  font-size: 12px;
  transition: transform 0.2s ease;
  color: var(--accent);
  margin-top: 5px;
}
details.step-card[open] summary::after {
  transform: rotate(-180deg);
}\;

css = css.replace(/details\.step-card \{[\s\S]*?details\.step-card\[open\] summary\.step-badge::after \{[\s\S]*?\}/, replacement);

fs.writeFileSync('style.css', css);
