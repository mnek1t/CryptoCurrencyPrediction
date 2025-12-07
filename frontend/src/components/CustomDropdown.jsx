export default function CustomDropdown({
  label,
  value,
  options,
  onChange,
}) {
  return (
    <div className="dropdown-container">
      {label && <span className="dropdown-label">{label}</span>}

      <select
        className="dropdown"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {options.map((o) => (
          <option key={o} value={o.toLowerCase()}>
            {o}
          </option>
        ))}
      </select>
    </div>
  );
}
