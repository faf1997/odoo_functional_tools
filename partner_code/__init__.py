from . import models 


# def assign_existing_customer_codes(env):
#     """
#     Assigns customer_code to existing partners without one.
#     """
#     partners = env['res.partner'].search([('customer_code', '=', False)])
#     for partner in partners:
#         code = env['ir.sequence'].next_by_code('res.partner.customer.code')
#         partner.sudo().write({'customer_code': code})



import logging

_logger = logging.getLogger(__name__)

def assign_existing_customer_codes(env):
    """
    Assigns customer_code to existing partners without one.
    Only assigns to actual customers (is_company=True or parent_id=False and customer_rank > 0).
    """
    _logger.info("Iniciando asignación de códigos de cliente a partners existentes")
    
    # Verificar que la secuencia existe
    sequence = env['ir.sequence'].search([('code', '=', 'res.partner.customer.code')], limit=1)
    if not sequence:
        _logger.info("Secuencia 'res.partner.customer.code' no encontrada, creando...")
        # Crear la secuencia si no existe
        env['ir.sequence'].create({
            'name': 'Customer Code',
            'code': 'res.partner.customer.code',
            'prefix': 'C',
            'padding': 5,
            'number_increment': 1,
        })
        _logger.info("Secuencia creada exitosamente")
    
    # Buscar solo partners que son clientes y no tienen código
    domain = [
        ('customer_code', '=', False),
        '|',
        ('is_company', '=', True),  # Empresas
        '&',
        ('parent_id', '=', False),  # Contactos principales (no hijos)
        ('customer_rank', '>', 0)   # Que sean clientes
    ]
    
    partners = env['res.partner'].search(domain)
    
    _logger.info(f"Encontrados {len(partners)} partners para asignar código")
    
    success_count = 0
    error_count = 0
    
    for partner in partners:
        try:
            code = env['ir.sequence'].next_by_code('res.partner.customer.code')
            if code:
                partner.sudo().write({'customer_code': code})
                _logger.info(f"Asignado código {code} a {partner.name} (ID: {partner.id})")
                success_count += 1
            else:
                _logger.warning(f"No se pudo generar código para {partner.name} (ID: {partner.id})")
                error_count += 1
        except Exception as e:
            _logger.error(f"Error asignando código a {partner.name} (ID: {partner.id}): {str(e)}")
            error_count += 1
    
    _logger.info(f"Proceso completado: {success_count} códigos asignados exitosamente, {error_count} errores")

