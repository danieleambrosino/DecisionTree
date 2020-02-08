from attributes import DiscreteAttribute, NumericAttribute, GoalAttribute

reduce_split_points = False
split_points_threshold = 2

training_set_file_path = 'datasets/adult.training'
validation_set_file_path = 'datasets/adult.validation'
test_set_file_path = 'datasets/adult.test'

goal = GoalAttribute(14, 'annual-income', ('<=50K', '>50K'), '>50K')

attributes = (
    NumericAttribute(0, 'age'),
    DiscreteAttribute(1, 'workclass', (
        'Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay')),
    NumericAttribute(2, 'fnlwgt'),
    DiscreteAttribute(3, 'education', (
        'Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th',
        '12th',
        'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool')),
    NumericAttribute(4, 'education-num'),
    DiscreteAttribute(5, 'marital-status', (
        'Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent',
        'Married-AF-spouse')),
    DiscreteAttribute(6, 'occupation', (
        'Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty',
        'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving',
        'Priv-house-serv', 'Protective-serv', 'Armed-Forces'
    )),
    DiscreteAttribute(7, 'relationship',
                      ('Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried')),
    DiscreteAttribute(8, 'race', ('White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black')),
    DiscreteAttribute(9, 'sex', ('Female', 'Male')),
    NumericAttribute(10, 'capital-gain'),
    NumericAttribute(11, 'capital-loss'),
    NumericAttribute(12, 'hours-per-week'),
    DiscreteAttribute(13, 'native-country', (
        'United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)',
        'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland',
        'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador',
        'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia',
        'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands'
    )),
    goal
)
