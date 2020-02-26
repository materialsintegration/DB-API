-- //////////////////////////////////////////////////////////////

/* 
  create creep test view

-- Usage:
--     call create_view_creep_test;
--
-- sample:
--     call create_view_creep_test()
--
*/

DROP PROCEDURE IF EXISTS create_view_creep_test;
delimiter '//'

CREATE PROCEDURE create_view_creep_test() 
BEGIN 
    
    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION, SQLWARNING 
    BEGIN
        GET DIAGNOSTICS CONDITION 1 
            @sqlstate = RETURNED_SQLSTATE, 
            @errno = MYSQL_ERRNO, 
            @text = MESSAGE_TEXT;
        SELECT @sqlstate, @errno, @text;
        ROLLBACK;
    END;


    START TRANSACTION;


    -- create view
    set group_concat_max_len = (40*1024);
    set @sql1 = "";
    select 
        group_concat(property_series) into @sql1 
    from 
    (
    select 
        concat(
            'vp.`', replace(pt.property_type_name, " ", "_"), '_min`,',
            'vp.`', replace(pt.property_type_name, " ", "_"), '_max`,',
            'vp.`', replace(pt.property_type_name, " ", "_"), '`,',
            'vp.`', replace(pt.property_type_name, " ", "_"), '_unit`'
    --        'vp.`', pt.property_type_name, '_temperature_min`,',
    --        'vp.`', pt.property_type_name, '_temperature_max`'
        ) property_series 
    from property p 
    left join property_type pt 
    on p.property_type_id = pt.property_type_id 
    left join test t 
    on t.test_piece_id = p.test_piece_id 
    left join test_type tt 
    on t.test_type_id = tt.test_type_id 
    left join creep_test ct 
    on t.test_id = ct.test_id 
    where tt.test_type_name = 'creep rupture test' 
    group by pt.property_type_name
    ) temp;


    set @sql = "";
    set @sql = concat(@sql, 'create or replace view view_creep_test ');
    set @sql = concat(@sql, 'as ');
    set @sql = concat(@sql, 'select ');
    set @sql = concat(@sql, '    tp.test_piece_id, ');
    set @sql = concat(@sql, '    ctt.creep_test_type_name, ');
    set @sql = concat(@sql, '    tp.material_id, ');
    set @sql = concat(@sql, '    ct.test_stress, ');
    set @sql = concat(@sql, '    ct.test_temperature_min, ');
    set @sql = concat(@sql, '    ct.test_temperature_max, ');
    set @sql = concat(@sql, '    (coalesce(ct.test_temperature_min, ct.test_temperature_max) + coalesce(ct.test_temperature_max, ct.test_temperature_max))/2 as "test_temperature",');
    set @sql = concat(@sql, '    ct.room_temperature, ');
    set @sql = concat(@sql, '    ct.test_atmosphere, ');
    set @sql = concat(@sql, '    ct.interruption_count, ');
    set @sql = concat(@sql, @sql1, ' ');
    set @sql = concat(@sql, 'from creep_test ct ');
    set @sql = concat(@sql, 'left join creep_test_type ctt ');
    set @sql = concat(@sql, 'on ct.creep_test_type_id = ctt.creep_test_type_id ');
    set @sql = concat(@sql, 'left join test t ');
    set @sql = concat(@sql, 'on ct.test_id = t.test_id ');
    set @sql = concat(@sql, 'and t.deleted is false ');
    set @sql = concat(@sql, 'left join test_piece tp ');
    set @sql = concat(@sql, 'on t.test_piece_id = tp.test_piece_id ');
    set @sql = concat(@sql, 'and tp.deleted is false ');
    set @sql = concat(@sql, 'left join view_property vp ');
    set @sql = concat(@sql, 'on t.test_piece_id = vp.test_piece_id');

    -- select @sql;

    if @sql is not null then
      prepare stmt from @sql;
      execute stmt;
      deallocate prepare stmt;

      -- transaction end
      -- ROLLBACK;
      COMMIT;
      SELECT 'Success!' as create_view_machine_learning FROM DUAL;
    else
      SELECT 'No action cause no data.' as create_view_machine_learning1 FROM DUAL;
    end if;
END;
//

delimiter ';'

