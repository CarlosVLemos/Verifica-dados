import os
import pandas as pd
import random
from faker import Faker

def gerar_dataset_se_nao_existir():
    path = "dataset/vazamentos.csv"


    if os.path.exists(path):
        return


    os.makedirs("dataset", exist_ok=True)

    fake = Faker('pt_BR')
    random.seed(42)

    columns = [
        "Nome", "Email", "cpf", "telefone", "Titulo", "Domain", "BreachDate",
        "AddedDate", "ModifiedDate", "PwnCount", "Description", "LogoPath",
        "DataClasses", "IsVerified", "IsFabricated", "IsSensitive", "IsRetired",
        "IsSpamList", "IsMalware", "IsSubscriptionFree"
    ]

    data = []
    for _ in range(100):
        nome = fake.name()
        email = fake.email()
        cpf = fake.cpf()
        telefone = fake.phone_number()
        titulo = fake.job()
        domain = email.split('@')[1]
        breach_date = fake.date_between(start_date='-5y', end_date='-1y')
        added_date = fake.date_between(start_date=breach_date, end_date='today')
        modified_date = fake.date_between(start_date=added_date, end_date='today')
        pwn_count = random.randint(1000, 10000000)
        description = fake.text(max_nb_chars=100)
        logo_path = f"https://logo.example.com/{domain}.png"
        data_classes = ', '.join(fake.words(nb=random.randint(1, 4)))
        flags = [random.choice([True, False]) for _ in range(7)]  

        data.append([
            nome, email, cpf, telefone, titulo, domain,
            breach_date, added_date, modified_date,
            pwn_count, description, logo_path, data_classes,
            *flags  
        ])

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')
