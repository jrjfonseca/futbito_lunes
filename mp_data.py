from mp_api.client import MPRester

with MPRester(api_key="sorNeGqPKtHSyd4u8o9ODl9Em96eJDJT") as mpr:
    thermo_docs = mpr.materials.thermo.search(material_ids=["mp-806082"])

    # In addition, you can specify the level of theory by using "thermo_type", the default is "GGA_GGA+U_R2SCAN":
    thermo_docs = mpr.materials.thermo.search(
        material_ids=["mp-806082"], thermo_types=["GGA_GGA+U", "GGA_GGA+U_R2SCAN", "R2SCAN"]
    )

    print(thermo_docs)


from mp_api.client import MPRester

with MPRester(api_key="sorNeGqPKtHSyd4u8o9ODl9Em96eJDJT") as mpr:
    tasks_doc = mpr.materials.tasks.search(
            ["mp-2740192"],           # task_id of this calculation
            fields=["task_id", "orig_inputs", "calcs_reversed", "output", "last_updated"]
        )

    print(tasks_doc)


from mp_api.client import MPRester

with MPRester(api_key="sorNeGqPKtHSyd4u8o9ODl9Em96eJDJT") as mpr:
    thermo_docs = mpr.materials.thermo.search(material_ids=["mp-19511"])

    # In addition, you can specify the level of theory by using "thermo_type", the default is "GGA_GGA+U_R2SCAN":
    thermo_docs = mpr.materials.thermo.search(
        material_ids=["mp-19511"], thermo_types=["GGA_GGA+U", "GGA_GGA+U_R2SCAN", "R2SCAN"]
    )

    print(thermo_docs)