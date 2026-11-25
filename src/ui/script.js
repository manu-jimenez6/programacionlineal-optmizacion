const tabs = [...document.querySelectorAll('[role="tab"]')];
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activateTab(tab));
      tab.addEventListener('keydown', event => {
        if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
        activateTab(tabs[next]); tabs[next].focus();
      });
    });
    function activateTab(selected) {
      tabs.forEach(tab => {
        const active = tab === selected;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
      });
    }

    const constraintList = document.getElementById('constraint-list');
    document.getElementById('add-constraint').addEventListener('click', () => {
      const rowNumber = constraintList.children.length + 1;
      const row = document.createElement('div');
      row.className = 'constraint-row';
      row.innerHTML = `<input class="field" type="number" aria-label="Coeficiente X1 de restricción ${rowNumber}" placeholder="0"><input class="field" type="number" aria-label="Coeficiente X2 de restricción ${rowNumber}" placeholder="0"><select aria-label="Operador de restricción ${rowNumber}"><option>≤</option><option>≥</option><option>=</option></select><input class="field" type="number" aria-label="Lado derecho de restricción ${rowNumber}" placeholder="0"><button class="delete-row" type="button" aria-label="Eliminar restricción ${rowNumber}" title="Eliminar fila">⌫</button>`;
      constraintList.append(row);
    });
    constraintList.addEventListener('click', event => {
      const button = event.target.closest('.delete-row');
      if (button) button.closest('.constraint-row').remove();
    });
    document.getElementById('clear-all').addEventListener('click', () => {
      document.querySelectorAll('#problem-form input[type="number"]').forEach(input => input.value = '');
      constraintList.replaceChildren();
    });

    const objectiveFields = document.getElementById('objective-fields');
    document.getElementById('add-variable').addEventListener('click', () => {
      const count = objectiveFields.querySelectorAll('.variable-label').length + 1;
      const plus = document.createElement('span'); plus.className = 'operator-plus'; plus.textContent = '+';
      const input = document.createElement('input'); input.className = 'field objective-input'; input.type = 'number'; input.placeholder = '0'; input.setAttribute('aria-label', `Coeficiente de X${count}`);
      const label = document.createElement('span'); label.className = 'variable-label'; label.textContent = `X${count}`;
      objectiveFields.append(plus, input, label);
    });
    document.getElementById('remove-variable').addEventListener('click', () => {
      const labels = objectiveFields.querySelectorAll('.variable-label');
      if (labels.length <= 1) return;
      const lastLabel = labels[labels.length - 1];
      lastLabel.previousElementSibling.remove(); // coefficient
      lastLabel.previousElementSibling.remove(); // plus sign
      lastLabel.remove();
    });

    const bigMTable = `<table class="matrix-table"><thead><tr><th>Base</th><th>Cb</th><th>X1</th><th>X2</th><th>S1</th><th>S2</th><th>S3</th><th>A1</th><th>RHS</th></tr></thead><tbody><tr><td><strong>S1</strong></td><td>0</td><td>2</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>100</td></tr><tr><td><strong>X2</strong></td><td>60</td><td>1</td><td>2</td><td>0</td><td>1</td><td>0</td><td>0</td><td>16</td></tr><tr><td><strong>S3</strong></td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>60</td></tr><tr><td><strong>Z</strong></td><td>—</td><td>80</td><td>60</td><td>0</td><td>0</td><td>0</td><td>M</td><td>3380</td></tr></tbody></table>`;
    const simplexContainer = document.getElementById('simplex-table-container');
    function updateSimplexTable() {
      const method = document.querySelector('input[name="method"]:checked').value;
      simplexContainer.innerHTML = method === 'bigm'
        ? bigMTable
        : '<p>El Simplex revisado calcula la solución usando la base y su inversa. El detalle de iteraciones se implementará en la vista paso a paso.</p>';
      document.getElementById('table-method-label').textContent = method === 'bigm' ? 'Método Gran M' : 'Método Simplex Revisado';
      document.querySelector('.status').textContent = method === 'bigm'
        ? 'Gran M · solución directa'
        : 'Simplex revisado · solución directa';
    }
    document.querySelectorAll('input[name="method"]').forEach(radio => radio.addEventListener('change', updateSimplexTable));
    updateSimplexTable();


// Mantiene las columnas de restricciones sincronizadas con las variables.
function syncConstraintColumns() {
  const variableNames = [...objectiveFields.querySelectorAll('.variable-label')].map(label => label.textContent);
  const header = document.querySelector('.constraint-head');
  header.replaceChildren();
  [...variableNames, 'Operador', 'RHS', ''].forEach(text => {
    const cell = document.createElement('span');
    cell.textContent = text;
    header.append(cell);
  });
  const columns = `repeat(${variableNames.length}, minmax(42px, 1fr)) 76px minmax(55px, 1fr) 34px`;
  header.style.gridTemplateColumns = columns;
  constraintList.querySelectorAll('.constraint-row').forEach((row, rowIndex) => {
    const operator = row.querySelector('select');
    while (row.querySelectorAll('input[type="number"]').length < variableNames.length + 1) {
      const coefficient = document.createElement('input');
      coefficient.className = 'field'; coefficient.type = 'number'; coefficient.placeholder = '0';
      const index = row.querySelectorAll('input[type="number"]').length;
      coefficient.setAttribute('aria-label', `Coeficiente de ${variableNames[index]} en restricción ${rowIndex + 1}`);
      row.insertBefore(coefficient, operator);
    }
    while (row.querySelectorAll('input[type="number"]').length > variableNames.length + 1) {
      const inputs = row.querySelectorAll('input[type="number"]');
      inputs[inputs.length - 2].remove();
    }
    row.style.gridTemplateColumns = columns;
    row.querySelectorAll('input[type="number"]').forEach((input, index) => {
      input.setAttribute('aria-label', index < variableNames.length ? `Coeficiente de ${variableNames[index]} en restricción ${rowIndex + 1}` : `Lado derecho de restricción ${rowIndex + 1}`);
    });
    row.querySelector('select').setAttribute('aria-label', `Operador de restricción ${rowIndex + 1}`);
    row.querySelector('.delete-row').setAttribute('aria-label', `Eliminar restricción ${rowIndex + 1}`);
  });
}

document.getElementById('add-variable').addEventListener('click', syncConstraintColumns);
document.getElementById('remove-variable').addEventListener('click', syncConstraintColumns);
document.getElementById('add-constraint').addEventListener('click', syncConstraintColumns);
syncConstraintColumns();

const problemForm = document.getElementById('problem-form');
const messageBanner = document.querySelector('.error-banner');
const showMessage = (message, isSuccess = false) => {
  messageBanner.textContent = message;
  messageBanner.classList.toggle('success', isSuccess);
  messageBanner.hidden = false;
};
problemForm.addEventListener('submit', async event => {
  event.preventDefault();
  const variableNames = [...objectiveFields.querySelectorAll('.variable-label')].map(label => label.textContent);
  const objectiveValues = [...objectiveFields.querySelectorAll('.objective-input')].map(input => input.value.trim());
  const rows = [...constraintList.querySelectorAll('.constraint-row')];
  const values = [...objectiveValues, ...rows.flatMap(row => [...row.querySelectorAll('input[type="number"]')].map(input => input.value.trim()))];
  if (values.some(value => value === '' || !Number.isFinite(Number(value)))) {
    showMessage('Error: completa todos los campos con valores numéricos.');
    return;
  }
  const sentido = document.querySelector('input[name="optimization"]:checked').value === 'max' ? 'maximizar' : 'minimizar';
  const metodo = document.querySelector('input[name="method"]:checked').value === 'revised'
    ? 'simplex_revisado' : 'gran_m';
  const payload = {
    metodo,
    variables: variableNames.map(nombre => ({ nombre, no_negativa: true })),
    funcion_objetivo: { sentido, coeficientes: objectiveValues },
    restricciones: rows.map(row => {
      const inputs = [...row.querySelectorAll('input[type="number"]')];
      const operator = row.querySelector('select').value;
      return {
        coeficientes: inputs.slice(0, variableNames.length).map(input => input.value.trim()),
        operador: { '≤': '<=', '≥': '>=' }[operator] || operator,
        lado_derecho: inputs[variableNames.length].value.trim()
      };
    })
  };
  try {
    const response = await fetch('/api/resolver', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.error || result.mensaje || 'No se pudo resolver el problema.');

    document.getElementById('solution-status').textContent = result.estado;
    if (result.estado === 'optimo') {
      document.getElementById('solution-variables').innerHTML = Object.entries(result.variables)
        .map(([nombre, valor]) => `<p class="metric-value">${nombre}: ${valor}</p>`).join('');
      document.getElementById('solution-z').textContent = result.z;
      document.getElementById('constraint-results').innerHTML = result.restricciones.map(r =>
        `<tr><td><strong>${r.nombre}</strong></td><td>${r.lado_derecho}</td><td>${r.usado}</td><td>${r.holgura_exceso}</td><td><span class="pill">${r.estado}</span></td></tr>`
      ).join('');
      showMessage(result.mensaje, true);
    } else {
      document.getElementById('solution-variables').innerHTML = '<p class="metric-value">—</p>';
      document.getElementById('solution-z').textContent = '—';
      document.getElementById('constraint-results').innerHTML = `<tr><td colspan="5">${result.mensaje}</td></tr>`;
      showMessage(result.mensaje);
    }
  } catch (error) {
    showMessage(`Error: ${error.message || 'No fue posible conectar con el servidor.'}`);
  }
});

