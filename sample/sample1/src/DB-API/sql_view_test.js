var sql = '';
sql = sql + 'select ';
sql = sql + '    vms.*, ';
sql = sql + '    vme.*, ';
sql = sql + '    vt.* ';
sql = sql + 'from __view__ vt ';
sql = sql + 'left join view_material_subset1 vms ';
sql = sql + 'on vt.material_id = vms.material_id ';
sql = sql + 'left join view_material_element vme ';
sql = sql + 'on vt.material_id = vme.material_id ';
sql = sql + 'order by vt.test_piece_id ';

module.exports = sql;
