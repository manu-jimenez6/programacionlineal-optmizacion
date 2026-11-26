"""Componente HTML del panel de iteraciones Paso a Paso."""

from markupsafe import Markup


def renderizar_paso_a_paso():
    """Construye el panel que JavaScript rellena con las iteraciones del API."""
    return Markup(
        '<section class="tab-panel" role="tabpanel" id="panel-steps" '
        'aria-labelledby="tab-steps" hidden>'
        '<article class="data-card">'
        '<div class="data-card-header">'
        '<h3>Iteraciones del método · datos simulados</h3>'
        '<span class="table-note" id="table-method-label">Método Gran M</span>'
        '</div>'
        '<div id="step-iterations" class="step-iterations" aria-live="polite">'
        '<p class="step-empty">Resuelve un problema para ver sus iteraciones.</p>'
        '</div>'
        '</article>'
        '</section>'
    )
