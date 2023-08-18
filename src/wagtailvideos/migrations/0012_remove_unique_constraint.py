# Generated by Django 2.2.17 on 2021-02-09 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailvideos', '0011_video_tracks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videotrack',
            name='language',
            field=models.CharField(blank=True, choices=[('aa', 'Afar'), ('aa-DJ', 'Afar - Djibouti'), ('aa-ER', 'Afar - Eritrea'), ('aa-ET', 'Afar - Ethiopia'), ('af', 'Afrikaans'), ('af-NA', 'Afrikaans - Namibia'), ('af-ZA', 'Afrikaans - South Africa'), ('agq', 'Aghem'), ('agq-CM', 'Aghem - Cameroon'), ('ak', 'Akan'), ('ak-GH', 'Akan - Ghana'), ('sq', 'Albanian'), ('sq-AL', 'Albanian - Albania'), ('sq-MK', 'Albanian - North Macedonia'), ('gsw', 'Alsatian'), ('gsw-FR', 'Alsatian - France'), ('gsw-LI', 'Alsatian - Liechtenstein'), ('gsw-CH', 'Alsatian - Switzerland'), ('am', 'Amharic'), ('am-ET', 'Amharic - Ethiopia'), ('ar', 'Arabic'), ('ar-DZ', 'Arabic - Algeria'), ('ar-BH', 'Arabic - Bahrain'), ('ar-TD', 'Arabic - Chad'), ('ar-KM', 'Arabic - Comoros'), ('ar-DJ', 'Arabic - Djibouti'), ('ar-EG', 'Arabic - Egypt'), ('ar-ER', 'Arabic - Eritrea'), ('ar-IQ', 'Arabic - Iraq'), ('ar-IL', 'Arabic - Israel'), ('ar-JO', 'Arabic - Jordan'), ('ar-KW', 'Arabic - Kuwait'), ('ar-LB', 'Arabic - Lebanon'), ('ar-LY', 'Arabic - Libya'), ('ar-MR', 'Arabic - Mauritania'), ('ar-MA', 'Arabic - Morocco'), ('ar-OM', 'Arabic - Oman'), ('ar-PS', 'Arabic - Palestinian Authority'), ('ar-QA', 'Arabic - Qatar'), ('ar-SA', 'Arabic - Saudi Arabia'), ('ar-SO', 'Arabic - Somalia'), ('ar-SS', 'Arabic - South Sudan'), ('ar-SD', 'Arabic - Sudan'), ('ar-SY', 'Arabic - Syria'), ('ar-TN', 'Arabic - Tunisia'), ('ar-AE', 'Arabic - U.A.E.'), ('ar-001', 'Arabic - World'), ('ar-YE', 'Arabic - Yemen'), ('hy', 'Armenian'), ('hy-AM', 'Armenian - Armenia'), ('as', 'Assamese'), ('as-IN', 'Assamese - India'), ('ast', 'Asturian'), ('ast-ES', 'Asturian - Spain'), ('asa', 'Asu'), ('asa-TZ', 'Asu - Tanzania'), ('az-Cyrl', 'Azerbaijani (Cyrillic)'), ('az-Cyrl-AZ', 'Azerbaijani (Cyrillic) - Azerbaijan'), ('az', 'Azerbaijani (Latin)'), ('az-Latn', 'Azerbaijani (Latin), Latn'), ('az-Latn-AZ', 'Azerbaijani (Latin) - Azerbaijan'), ('ksf', 'Bafia'), ('ksf-CM', 'Bafia - Cameroon'), ('bm', 'Bamanankan'), ('bm-Latn-ML', 'Bamanankan (Latin) - Mali'), ('bn', 'Bangla'), ('bn-BD', 'Bangla - Bangladesh'), ('bn-IN', 'Bangla - India'), ('bas', 'Basaa'), ('bas-CM', 'Basaa - Cameroon'), ('ba', 'Bashkir'), ('ba-RU', 'Bashkir - Russia'), ('eu', 'Basque'), ('eu-ES', 'Basque - Spain'), ('be', 'Belarusian'), ('be-BY', 'Belarusian - Belarus'), ('bem', 'Bemba'), ('bem-ZM', 'Bemba - Zambia'), ('bez', 'Bena'), ('bez-TZ', 'Bena - Tanzania'), ('byn', 'Blin'), ('byn-ER', 'Blin - Eritrea'), ('brx', 'Bodo'), ('brx-IN', 'Bodo - India'), ('bs-Cyrl', 'Bosnian (Cyrillic)'), ('bs-Cyrl-BA', 'Bosnian (Cyrillic) - Bosnia and Herzegovina'), ('bs', 'Bosnian (Latin)'), ('bs-Latn', 'Bosnian (Latin), Latn'), ('bs-Latn-BA', 'Bosnian (Latin) - Bosnia and Herzegovina'), ('br', 'Breton'), ('br-FR', 'Breton - France'), ('bg', 'Bulgarian'), ('bg-BG', 'Bulgarian - Bulgaria'), ('my', 'Burmese'), ('my-MM', 'Burmese - Myanmar'), ('ca', 'Catalan'), ('ca-AD', 'Catalan - Andorra'), ('ca-FR', 'Catalan - France'), ('ca-IT', 'Catalan - Italy'), ('ca-ES', 'Catalan - Spain'), ('ceb', 'Cebuano'), ('ceb-Latn', 'Cebuan (Latin)'), ('ceb-Latn-PH', 'Cebuan (Latin) - Philippines'), ('tzm-Latn-MA', 'Central Atlas Tamazight (Latin) - Morocco'), ('ku', 'Central Kurdish'), ('ku-Arab', 'Central Kurdish, Arab'), ('ku-Arab-IQ', 'Central Kurdish - Iraq'), ('ccp', 'Chakma'), ('ccp-Cakm', 'Chakma - Chakma'), ('ccp-Cakm-BD', 'Chakma - Bangladesh'), ('ccp-Cakm-IN', 'Chakma - India'), ('cd-RU', 'Chechen - Russia'), ('chr', 'Cherokee'), ('chr-Cher', 'Cherokee, Cher'), ('chr-Cher-US', 'Cherokee - United States'), ('cgg', 'Chiga'), ('cgg-UG', 'Chiga - Uganda'), ('zh', 'Chinese (Simplified)'), ('zh-Hans', 'Chinese (Simplified), Hans'), ('zh-CN', "Chinese (Simplified) - People's Republic of China"), ('zh-SG', 'Chinese (Simplified) - Singapore'), ('zh-Hant', 'Chinese (Traditional)'), ('zh-HK', 'Chinese (Traditional) - Hong Kong S.A.R.'), ('zh-MO', 'Chinese (Traditional) - Macao S.A.R.'), ('zh-TW', 'Chinese (Traditional) - Taiwan'), ('cu-RU', 'Church Slavic - Russia'), ('swc', 'Congo Swahili'), ('swc-CD', 'Congo Swahili - Congo DRC'), ('kw', 'Cornish'), ('kw-GB', 'Cornish - United Kingdom'), ('co', 'Corsican'), ('co-FR', 'Corsican - France'), ('hr,', 'Croatian'), ('hr-HR', 'Croatian - Croatia'), ('hr-BA', 'Croatian (Latin) - Bosnia and Herzegovina'), ('cs', 'Czech'), ('cs-CZ', 'Czech - Czech Republic'), ('da', 'Danish'), ('da-DK', 'Danish - Denmark'), ('da-GL', 'Danish - Greenland'), ('prs', 'Dari'), ('prs-AF', 'Dari - Afghanistan'), ('dv', 'Divehi'), ('dv-MV', 'Divehi - Maldives'), ('dua', 'Duala'), ('dua-CM', 'Duala - Cameroon'), ('nl', 'Dutch'), ('nl-AW', 'Dutch - Aruba'), ('nl-BE', 'Dutch - Belgium'), ('nl-BQ', 'Dutch - Bonaire, Sint Eustatius and Saba'), ('nl-CW', 'Dutch - Curaçao'), ('nl-NL', 'Dutch - Netherlands'), ('nl-SX', 'Dutch - Sint Maarten'), ('nl-SR', 'Dutch - Suriname'), ('dz', 'Dzongkha'), ('dz-BT', 'Dzongkha - Bhutan'), ('ebu', 'Embu'), ('ebu-KE', 'Embu - Kenya'), ('en', 'English'), ('en-AS', 'English - American Samoa'), ('en-AI', 'English - Anguilla'), ('en-AG', 'English - Antigua and Barbuda'), ('en-AU', 'English - Australia'), ('en-AT', 'English - Austria'), ('en-BS', 'English - Bahamas'), ('en-BB', 'English - Barbados'), ('en-BE', 'English - Belgium'), ('en-BZ', 'English - Belize'), ('en-BM', 'English - Bermuda'), ('en-BW', 'English - Botswana'), ('en-IO', 'English - British Indian Ocean Territory'), ('en-VG', 'English - British Virgin Islands'), ('en-BI', 'English - Burundi'), ('en-CM', 'English - Cameroon'), ('en-CA', 'English - Canada'), ('en-029', 'English - Caribbean'), ('en-KY', 'English - Cayman Islands'), ('en-CX', 'English - Christmas Island'), ('en-CC', 'English - Cocos [Keeling] Islands'), ('en-CK', 'English - Cook Islands'), ('en-CY', 'English - Cyprus'), ('en-DK', 'English - Denmark'), ('en-DM', 'English - Dominica'), ('en-ER', 'English - Eritrea'), ('en-150', 'English - Europe'), ('en-FK', 'English - Falkland Islands'), ('en-FI', 'English - Finland'), ('en-FJ', 'English - Fiji'), ('en-GM', 'English - Gambia'), ('en-DE', 'English - Germany'), ('en-GH', 'English - Ghana'), ('en-GI', 'English - Gibraltar'), ('en-GD', 'English - Grenada'), ('en-GU', 'English - Guam'), ('en-GG', 'English - Guernsey'), ('en-GY', 'English - Guyana'), ('en-HK', 'English - Hong Kong'), ('en-IN', 'English - India'), ('en-IE', 'English - Ireland'), ('en-IM', 'English - Isle of Man'), ('en-IL', 'English - Israel'), ('en-JM', 'English - Jamaica'), ('en-JE', 'English - Jersey'), ('en-KE', 'English - Kenya'), ('en-KI', 'English - Kiribati'), ('en-LS', 'English - Lesotho'), ('en-LR', 'English - Liberia'), ('en-MO', 'English - Macao SAR'), ('en-MG', 'English - Madagascar'), ('en-MW', 'English - Malawi'), ('en-MY', 'English - Malaysia'), ('en-MT', 'English - Malta'), ('en-MH', 'English - Marshall Islands'), ('en-MU', 'English - Mauritius'), ('en-FM', 'English - Micronesia'), ('en-MS', 'English - Montserrat'), ('en-NA', 'English - Namibia'), ('en-NR', 'English - Nauru'), ('en-NL', 'English - Netherlands'), ('en-NZ', 'English - New Zealand'), ('en-NG', 'English - Nigeria'), ('en-NU', 'English - Niue'), ('en-NF', 'English - Norfolk Island'), ('en-MP', 'English - Northern Mariana Islands'), ('en-PK', 'English - Pakistan'), ('en-PW', 'English - Palau'), ('en-PG', 'English - Papua New Guinea'), ('en-PN', 'English - Pitcairn Islands'), ('en-PR', 'English - Puerto Rico'), ('en-PH', 'English - Republic of the Philippines'), ('en-RW', 'English - Rwanda'), ('en-KN', 'English - Saint Kitts and Nevis'), ('en-LC', 'English - Saint Lucia'), ('en-VC', 'English - Saint Vincent and the Grenadines'), ('en-WS', 'English - Samoa'), ('en-SC', 'English - Seychelles'), ('en-SL', 'English - Sierra Leone'), ('en-SG', 'English - Singapore'), ('en-SX', 'English - Sint Maarten'), ('en-SI', 'English - Slovenia'), ('en-SB', 'English - Solomon Islands'), ('en-ZA', 'English - South Africa'), ('en-SS', 'English - South Sudan'), ('en-SH', 'English - St Helena, Ascension, Tristan da Cunha'), ('en-SD', 'English - Sudan'), ('en-SZ', 'English - Swaziland'), ('en-SE', 'English - Sweden'), ('en-CH', 'English - Switzerland'), ('en-TZ', 'English - Tanzania'), ('en-TK', 'English - Tokelau'), ('en-TO', 'English - Tonga'), ('en-TT', 'English - Trinidad and Tobago'), ('en-TC', 'English - Turks and Caicos Islands'), ('en-TV', 'English - Tuvalu'), ('en-UG', 'English - Uganda'), ('en-AE', 'English - United Arab Emirates'), ('en-GB', 'English - United Kingdom'), ('en-US', 'English - United States'), ('en-UM', 'English - US Minor Outlying Islands'), ('en-VI', 'English - US Virgin Islands'), ('en-VU', 'English - Vanuatu'), ('en-001', 'English - World'), ('en-ZM', 'English - Zambia'), ('en-ZW', 'English - Zimbabwe'), ('eo', 'Esperanto'), ('eo-001', 'Esperanto - World'), ('et', 'Estonian'), ('et-EE', 'Estonian - Estonia'), ('ee', 'Ewe'), ('ee-GH', 'Ewe - Ghana'), ('ee-TG', 'Ewe - Togo'), ('ewo', 'Ewondo'), ('ewo-CM', 'Ewondo - Cameroon'), ('fo', 'Faroese'), ('fo-DK', 'Faroese - Denmark'), ('fo-FO', 'Faroese - Faroe Islands'), ('fil', 'Filipino'), ('fil-PH', 'Filipino - Philippines'), ('fi', 'Finnish'), ('fi-FI', 'Finnish - Finland'), ('fr', 'French'), ('fr-DZ', 'French - Algeria'), ('fr-BE', 'French - Belgium'), ('fr-BJ', 'French - Benin'), ('fr-BF', 'French - Burkina Faso'), ('fr-BI', 'French - Burundi'), ('fr-CM', 'French - Cameroon'), ('fr-CA', 'French - Canada'), ('fr-CF', 'French - Central African Republic'), ('fr-TD', 'French - Chad'), ('fr-KM', 'French - Comoros'), ('fr-CG', 'French - Congo'), ('fr-CD', 'French - Congo, DRC'), ('fr-CI', "French - Côte d'Ivoire"), ('fr-DJ', 'French - Djibouti'), ('fr-GQ', 'French - Equatorial Guinea'), ('fr-FR', 'French - France'), ('fr-GF', 'French - French Guiana'), ('fr-PF', 'French - French Polynesia'), ('fr-GA', 'French - Gabon'), ('fr-GP', 'French - Guadeloupe'), ('fr-GN', 'French - Guinea'), ('fr-HT', 'French - Haiti'), ('fr-LU', 'French - Luxembourg'), ('fr-MG', 'French - Madagascar'), ('fr-ML', 'French - Mali'), ('fr-MQ', 'French - Martinique'), ('fr-MR', 'French - Mauritania'), ('fr-MU', 'French - Mauritius'), ('fr-YT', 'French - Mayotte'), ('fr-MA', 'French - Morocco'), ('fr-NC', 'French - New Caledonia'), ('fr-NE', 'French - Niger'), ('fr-MC', 'French - Principality of Monaco'), ('fr-RE', 'French - Reunion'), ('fr-RW', 'French - Rwanda'), ('fr-BL', 'French - Saint Barthélemy'), ('fr-MF', 'French - Saint Martin'), ('fr-PM', 'French - Saint Pierre and Miquelon'), ('fr-SN', 'French - Senegal'), ('fr-SC', 'French - Seychelles'), ('fr-CH', 'French - Switzerland'), ('fr-SY', 'French - Syria'), ('fr-TG', 'French - Togo'), ('fr-TN', 'French - Tunisia'), ('fr-VU', 'French - Vanuatu'), ('fr-WF', 'French - Wallis and Futuna'), ('fy', 'Frisian'), ('fy-NL', 'Frisian - Netherlands'), ('fur', 'Friulian'), ('fur-IT', 'Friulian - Italy'), ('ff', 'Fulah'), ('ff-Latn', 'Fulah (Latin)'), ('ff-Latn-BF', 'Fulah (Latin) - Burkina Faso'), ('ff-CM', 'Fulah - Cameroon'), ('ff-Latn-CM', 'Fulah (Latin) - Cameroon'), ('ff-Latn-GM', 'Fulah (Latin) - Gambia'), ('ff-Latn-GH', 'Fulah (Latin) - Ghana'), ('ff-GN', 'Fulah - Guinea'), ('ff-Latn-GN', 'Fulah (Latin) - Guinea'), ('ff-Latn-GW', 'Fulah (Latin) - Guinea-Bissau'), ('ff-Latn-LR', 'Fulah (Latin) - Liberia'), ('ff-MR', 'Fulah - Mauritania'), ('ff-Latn-MR', 'Fulah (Latin) - Mauritania'), ('ff-Latn-NE', 'Fulah (Latin) - Niger'), ('ff-NG', 'Fulah - Nigeria'), ('ff-Latn-NG', 'Fulah (Latin) - Nigeria'), ('ff-Latn-SN', 'Fulah - Senegal'), ('ff-Latn-SL', 'Fulah (Latin) - Sierra Leone'), ('gl', 'Galician'), ('gl-ES', 'Galician - Spain'), ('lg', 'Ganda'), ('lg-UG', 'Ganda - Uganda'), ('ka', 'Georgian'), ('ka-GE', 'Georgian - Georgia'), ('de', 'German'), ('de-AT', 'German - Austria'), ('de-BE', 'German - Belgium'), ('de-DE', 'German - Germany'), ('de-IT', 'German - Italy'), ('de-LI', 'German - Liechtenstein'), ('de-LU', 'German - Luxembourg'), ('de-CH', 'German - Switzerland'), ('el', 'Greek'), ('el-CY', 'Greek - Cyprus'), ('el-GR', 'Greek - Greece'), ('kl', 'Greenlandic'), ('kl-GL', 'Greenlandic - Greenland'), ('gn', 'Guarani'), ('gn-PY', 'Guarani - Paraguay'), ('gu', 'Gujarati'), ('gu-IN', 'Gujarati - India'), ('guz', 'Gusii'), ('guz-KE', 'Gusii - Kenya'), ('ha', 'Hausa (Latin)'), ('ha-Latn', 'Hausa (Latin), Latn'), ('ha-Latn-GH', 'Hausa (Latin) - Ghana'), ('ha-Latn-NE', 'Hausa (Latin) - Niger'), ('ha-Latn-NG', 'Hausa (Latin) - Nigeria'), ('haw', 'Hawaiian'), ('haw-US', 'Hawaiian - United States'), ('he', 'Hebrew'), ('he-IL', 'Hebrew - Israel'), ('hi', 'Hindi'), ('hi-IN', 'Hindi - India'), ('hu', 'Hungarian'), ('hu-HU', 'Hungarian - Hungary'), ('is', 'Icelandic'), ('is-IS', 'Icelandic - Iceland'), ('ig', 'Igbo'), ('ig-NG', 'Igbo - Nigeria'), ('id', 'Indonesian'), ('id-ID', 'Indonesian - Indonesia'), ('ia', 'Interlingua'), ('ia-FR', 'Interlingua - France'), ('ia-001', 'Interlingua - World'), ('iu', 'Inuktitut (Latin)'), ('iu-Latn', 'Inuktitut (Latin), Latn'), ('iu-Latn-CA', 'Inuktitut (Latin) - Canada'), ('iu-Cans', 'Inuktitut (Syllabics)'), ('iu-Cans-CA', 'Inuktitut (Syllabics) - Canada'), ('ga', 'Irish'), ('ga-IE', 'Irish - Ireland'), ('it', 'Italian'), ('it-IT', 'Italian - Italy'), ('it-SM', 'Italian - San Marino'), ('it-CH', 'Italian - Switzerland'), ('it-VA', 'Italian - Vatican City'), ('ja', 'Japanese'), ('ja-JP', 'Japanese - Japan'), ('jv', 'Javanese'), ('jv-Latn', 'Javanese - Latin'), ('jv-Latn-ID', 'Javanese - Latin, Indonesia'), ('dyo', 'Jola-Fonyi'), ('dyo-SN', 'Jola-Fonyi - Senegal'), ('kea', 'Kabuverdianu'), ('kea-CV', 'Kabuverdianu - Cabo Verde'), ('kab', 'Kabyle'), ('kab-DZ', 'Kabyle - Algeria'), ('kkj', 'Kako'), ('kkj-CM', 'Kako - Cameroon'), ('kln', 'Kalenjin'), ('kln-KE', 'Kalenjin - Kenya'), ('kam', 'Kamba'), ('kam-KE', 'Kamba - Kenya'), ('kn', 'Kannada'), ('kn-IN', 'Kannada - India'), ('ks', 'Kashmiri'), ('ks-Arab', 'Kashmiri - Perso-Arabic'), ('ks-Arab-IN', 'Kashmiri - Perso-Arabic, IN'), ('kk', 'Kazakh'), ('kk-KZ', 'Kazakh - Kazakhstan'), ('km', 'Khmer'), ('km-KH', 'Khmer - Cambodia'), ('quc', "K'iche"), ('quc-Latn-GT', "K'iche - Guatemala"), ('ki', 'Kikuyu'), ('ki-KE', 'Kikuyu - Kenya'), ('rw', 'Kinyarwanda'), ('rw-RW', 'Kinyarwanda - Rwanda'), ('sw', 'Kiswahili'), ('sw-KE', 'Kiswahili - Kenya'), ('sw-TZ', 'Kiswahili - Tanzania'), ('sw-UG', 'Kiswahili - Uganda'), ('kok', 'Konkani'), ('kok-IN', 'Konkani - India'), ('ko', 'Korean'), ('ko-KR', 'Korean - Korea'), ('ko-KP', 'Korean - North Korea'), ('khq', 'Koyra Chiini'), ('khq-ML', 'Koyra Chiini - Mali'), ('ses', 'Koyraboro Senni'), ('ses-ML', 'Koyraboro Senni - Mali'), ('nmg', 'Kwasio'), ('nmg-CM', 'Kwasio - Cameroon'), ('ky', 'Kyrgyz'), ('ky-KG', 'Kyrgyz - Kyrgyzstan'), ('ku-Arab-IR', 'Kurdish - Perso-Arabic, Iran'), ('lkt', 'Lakota'), ('lkt-US', 'Lakota - United States'), ('lag', 'Langi'), ('lag-TZ', 'Langi - Tanzania'), ('lo', 'Lao'), ('lo-LA', 'Lao - Lao P.D.R.'), ('lv', 'Latvian'), ('lv-LV', 'Latvian - Latvia'), ('ln', 'Lingala'), ('ln-AO', 'Lingala - Angola'), ('ln-CF', 'Lingala - Central African Republic'), ('ln-CG', 'Lingala - Congo'), ('ln-CD', 'Lingala - Congo DRC'), ('lt', 'Lithuanian'), ('lt-LT', 'Lithuanian - Lithuania'), ('nds', 'Low German'), ('nds-DE', 'Low German - Germany'), ('nds-NL', 'Low German - Netherlands'), ('dsb', 'Lower Sorbian'), ('dsb-DE', 'Lower Sorbian - Germany'), ('lu', 'Luba-Katanga'), ('lu-CD', 'Luba-Katanga - Congo DRC'), ('luo', 'Luo'), ('luo-KE', 'Luo - Kenya'), ('lb', 'Luxembourgish'), ('lb-LU', 'Luxembourgish - Luxembourg'), ('luy', 'Luyia'), ('luy-KE', 'Luyia - Kenya'), ('mk', 'Macedonian'), ('mk-MK', 'Macedonian - North Macedonia'), ('jmc', 'Machame'), ('jmc-TZ', 'Machame - Tanzania'), ('mgh', 'Makhuwa-Meetto'), ('mgh-MZ', 'Makhuwa-Meetto - Mozambique'), ('kde', 'Makonde'), ('kde-TZ', 'Makonde - Tanzania'), ('mg', 'Malagasy'), ('mg-MG', 'Malagasy - Madagascar'), ('ms', 'Malay'), ('ms-BN', 'Malay - Brunei Darussalam'), ('ms-MY', 'Malay - Malaysia'), ('ml', 'Malayalam'), ('ml-IN', 'Malayalam - India'), ('mt', 'Maltese'), ('mt-MT', 'Maltese - Malta'), ('gv', 'Manx'), ('gv-IM', 'Manx - Isle of Man'), ('mi', 'Maori'), ('mi-NZ', 'Maori - New Zealand'), ('arn', 'Mapudungun'), ('arn-CL', 'Mapudungun - Chile'), ('mr', 'Marathi'), ('mr-IN', 'Marathi - India'), ('mas', 'Masai'), ('mas-KE', 'Masai - Kenya'), ('mas-TZ', 'Masai - Tanzania'), ('mzn-IR', 'Mazanderani - Iran'), ('mer', 'Meru'), ('mer-KE', 'Meru - Kenya'), ('mgo', "Meta'"), ('mgo-CM', "Meta' - Cameroon"), ('moh', 'Mohawk'), ('moh-CA', 'Mohawk - Canada'), ('mn', 'Mongolian (Cyrillic)'), ('mn-Cyrl', 'Mongolian (Cyrillic), Cyrl'), ('mn-MN', 'Mongolian (Cyrillic) - Mongolia'), ('mn-Mong', 'Mongolian (Traditional Mongolian)'), ('mn-Mong-CN', "Mongolian (Traditional Mongolian) - People's Republic of China"), ('mn-Mong-MN', 'Mongolian (Traditional Mongolian) - Mongolia'), ('mfe', 'Morisyen'), ('mfe-MU', 'Morisyen - Mauritius'), ('mua', 'Mundang'), ('mua-CM', 'Mundang - Cameroon'), ('nqo', "N'ko"), ('nqo-GN', "N'ko - Guinea"), ('naq', 'Nama'), ('naq-NA', 'Nama - Namibia'), ('ne', 'Nepali'), ('ne-IN', 'Nepali - India'), ('ne-NP', 'Nepali - Nepal'), ('nnh', 'Ngiemboon'), ('nnh-CM', 'Ngiemboon - Cameroon'), ('jgo', 'Ngomba'), ('jgo-CM', 'Ngomba - Cameroon'), ('lrc-IQ', 'Northern Luri - Iraq'), ('lrc-IR', 'Northern Luri - Iran'), ('nd', 'North Ndebele'), ('nd-ZW', 'North Ndebele - Zimbabwe'), ('no', 'Norwegian (Bokmal)'), ('nb', 'Norwegian (Bokmal), nb'), ('nb-NO', 'Norwegian (Bokmal) - Norway'), ('nn', 'Norwegian (Nynorsk)'), ('nn-NO', 'Norwegian (Nynorsk) - Norway'), ('nb-SJ', 'Norwegian Bokmål - Svalbard and Jan Mayen'), ('nus', 'Nuer'), ('nus-SD', 'Nuer - Sudan'), ('nus-SS', 'Nuer - South Sudan'), ('nyn', 'Nyankole'), ('nyn-UG', 'Nyankole - Uganda'), ('oc', 'Occitan'), ('oc-FR', 'Occitan - France'), ('or', 'Odia'), ('or-IN', 'Odia - India'), ('om', 'Oromo'), ('om-ET', 'Oromo - Ethiopia'), ('om-KE', 'Oromo - Kenya'), ('os', 'Ossetian'), ('os-GE', 'Ossetian - Cyrillic, Georgia'), ('os-RU', 'Ossetian - Cyrillic, Russia'), ('ps', 'Pashto'), ('ps-AF', 'Pashto - Afghanistan'), ('ps-PK', 'Pashto - Pakistan'), ('fa', 'Persian'), ('fa-AF', 'Persian - Afghanistan'), ('fa-IR', 'Persian - Iran'), ('pl', 'Polish'), ('pl-PL', 'Polish - Poland'), ('pt', 'Portuguese'), ('pt-AO', 'Portuguese - Angola'), ('pt-BR', 'Portuguese - Brazil'), ('pt-CV', 'Portuguese - Cabo Verde'), ('pt-GQ', 'Portuguese - Equatorial Guinea'), ('pt-GW', 'Portuguese - Guinea-Bissau'), ('pt-LU', 'Portuguese - Luxembourg'), ('pt-MO', 'Portuguese - Macao SAR'), ('pt-MZ', 'Portuguese - Mozambique'), ('pt-PT', 'Portuguese - Portugal'), ('pt-ST', 'Portuguese - São Tomé and Príncipe'), ('pt-CH', 'Portuguese - Switzerland'), ('pt-TL', 'Portuguese - Timor-Leste'), ('prg-001', 'Prussian'), ('qps-ploca', 'Pseudo Language - Pseudo locale for east Asian/complex script localization testing'), ('qps-ploc', 'Pseudo Language - Pseudo locale used for localization testing'), ('qps-plocm', 'Pseudo Language - Pseudo locale used for localization testing of mirroredlocales'), ('pa', 'Punjabi'), ('pa-Arab', 'Punjabi, Arab'), ('pa-IN', 'Punjabi - India'), ('pa-Arab-PK', 'Punjabi - Islamic Republic of Pakistan'), ('quz', 'Quechua'), ('quz-BO', 'Quechua - Bolivia'), ('quz-EC', 'Quechua - Ecuador'), ('quz-PE', 'Quechua - Peru'), ('ksh', 'Ripuarian'), ('ksh-DE', 'Ripuarian - Germany'), ('ro', 'Romanian'), ('ro-MD', 'Romanian - Moldova'), ('ro-RO', 'Romanian - Romania'), ('rm', 'Romansh'), ('rm-CH', 'Romansh - Switzerland'), ('rof', 'Rombo'), ('rof-TZ', 'Rombo - Tanzania'), ('rn', 'Rundi'), ('rn-BI', 'Rundi - Burundi'), ('ru', 'Russian'), ('ru-BY', 'Russian - Belarus'), ('ru-KZ', 'Russian - Kazakhstan'), ('ru-KG', 'Russian - Kyrgyzstan'), ('ru-MD', 'Russian - Moldova'), ('ru-RU', 'Russian - Russia'), ('ru-UA', 'Russian - Ukraine'), ('rwk', 'Rwa'), ('rwk-TZ', 'Rwa - Tanzania'), ('ssy', 'Saho'), ('ssy-ER', 'Saho - Eritrea'), ('sah', 'Sakha'), ('sah-RU', 'Sakha - Russia'), ('saq', 'Samburu'), ('saq-KE', 'Samburu - Kenya'), ('smn', 'Sami (Inari)'), ('smn-FI', 'Sami (Inari) - Finland'), ('smj', 'Sami (Lule)'), ('smj-NO', 'Sami (Lule) - Norway'), ('smj-SE', 'Sami (Lule) - Sweden'), ('se', 'Sami (Northern)'), ('se-FI', 'Sami (Northern) - Finland'), ('se-NO', 'Sami (Northern) - Norway'), ('se-SE', 'Sami (Northern) - Sweden'), ('sms', 'Sami (Skolt)'), ('sms-FI', 'Sami (Skolt) - Finland'), ('sma', 'Sami (Southern)'), ('sma-NO', 'Sami (Southern) - Norway'), ('sma-SE', 'Sami (Southern) - Sweden'), ('sg', 'Sango'), ('sg-CF', 'Sango - Central African Republic'), ('sbp', 'Sangu'), ('sbp-TZ', 'Sangu - Tanzania'), ('sa', 'Sanskrit'), ('sa-IN', 'Sanskrit - India'), ('gd', 'Scottish Gaelic'), ('gd-GB', 'Scottish Gaelic - United Kingdom'), ('seh', 'Sena'), ('seh-MZ', 'Sena - Mozambique'), ('sr-Cyrl', 'Serbian (Cyrillic)'), ('sr-Cyrl-BA', 'Serbian (Cyrillic) - Bosnia and Herzegovina'), ('sr-Cyrl-ME', 'Serbian (Cyrillic) - Montenegro'), ('sr-Cyrl-RS', 'Serbian (Cyrillic) - Serbia'), ('sr-Cyrl-CS', 'Serbian (Cyrillic) - Serbia and Montenegro (Former)'), ('sr', 'Serbian (Latin)'), ('sr-Latn', 'Serbian (Latin), Latn'), ('sr-Latn-BA', 'Serbian (Latin) - Bosnia and Herzegovina'), ('sr-Latn-ME', 'Serbian (Latin) - Montenegro'), ('sr-Latn-RS', 'Serbian (Latin) - Serbia'), ('sr-Latn-CS', 'Serbian (Latin) - Serbia and Montenegro (Former)'), ('nso', 'Sesotho sa Leboa'), ('nso-ZA', 'Sesotho sa Leboa - South Africa'), ('tn', 'Setswana'), ('tn-BW', 'Setswana - Botswana'), ('tn-ZA', 'Setswana - South Africa'), ('ksb', 'Shambala'), ('ksb-TZ', 'Shambala - Tanzania'), ('sn', 'Shona'), ('sn-Latn', 'Shona - Latin'), ('sn-Latn-ZW', 'Shona - Zimbabwe'), ('sd', 'Sindhi'), ('sd-Arab', 'Sindhi, Arab'), ('sd-Arab-PK', 'Sindhi - Islamic Republic of Pakistan'), ('si', 'Sinhala'), ('si-LK', 'Sinhala - Sri Lanka'), ('sk', 'Slovak'), ('sk-SK', 'Slovak - Slovakia'), ('sl', 'Slovenian'), ('sl-SI', 'Slovenian - Slovenia'), ('xog', 'Soga'), ('xog-UG', 'Soga - Uganda'), ('so', 'Somali'), ('so-DJ', 'Somali - Djibouti'), ('so-ET', 'Somali - Ethiopia'), ('so-KE', 'Somali - Kenya'), ('so-SO', 'Somali - Somalia'), ('st', 'Sotho'), ('st-ZA', 'Sotho - South Africa'), ('nr', 'South Ndebele'), ('nr-ZA', 'South Ndebele - South Africa'), ('st-LS', 'Southern Sotho - Lesotho'), ('es', 'Spanish'), ('es-AR', 'Spanish - Argentina'), ('es-BZ', 'Spanish - Belize'), ('es-VE', 'Spanish - Bolivarian Republic of Venezuela'), ('es-BO', 'Spanish - Bolivia'), ('es-BR', 'Spanish - Brazil'), ('es-CL', 'Spanish - Chile'), ('es-CO', 'Spanish - Colombia'), ('es-CR', 'Spanish - Costa Rica'), ('es-CU', 'Spanish - Cuba'), ('es-DO', 'Spanish - Dominican Republic'), ('es-EC', 'Spanish - Ecuador'), ('es-SV', 'Spanish - El Salvador'), ('es-GQ', 'Spanish - Equatorial Guinea'), ('es-GT', 'Spanish - Guatemala'), ('es-HN', 'Spanish - Honduras'), ('es-419', 'Spanish - Latin America'), ('es-MX', 'Spanish - Mexico'), ('es-NI', 'Spanish - Nicaragua'), ('es-PA', 'Spanish - Panama'), ('es-PY', 'Spanish - Paraguay'), ('es-PE', 'Spanish - Peru'), ('es-PH', 'Spanish - Philippines'), ('es-PR', 'Spanish - Puerto Rico'), ('es-ES', 'Spanish - Spain'), ('es-ES_tradnl', 'Spanish - Spain, ES_tradnl'), ('es-US', 'Spanish - United - States'), ('es-UY', 'Spanish - Uruguay'), ('zgh', 'Standard Moroccan Tamazight'), ('zgh-Tfng-MA', 'Standard Moroccan Tamazight - Morocco'), ('zgh-Tfng', 'Standard Moroccan Tamazight - Tifinagh'), ('ss', 'Swati'), ('ss-ZA', 'Swati - South Africa'), ('ss-SZ', 'Swati - Swaziland'), ('sv', 'Swedish'), ('sv-AX', 'Swedish - Åland Islands'), ('sv-FI', 'Swedish - Finland'), ('sv-SE', 'Swedish - Sweden'), ('syr', 'Syriac'), ('syr-SY', 'Syriac - Syria'), ('shi', 'Tachelhit'), ('shi-Tfng', 'Tachelhit - Tifinagh'), ('shi-Tfng-MA', 'Tachelhit - Tifinagh, Morocco'), ('shi-Latn', 'Tachelhit (Latin)'), ('shi-Latn-MA', 'Tachelhit (Latin) - Morocco'), ('dav', 'Taita'), ('dav-KE', 'Taita - Kenya'), ('tg', 'Tajik (Cyrillic)'), ('tg-Cyrl', 'Tajik (Cyrillic), Cyrl'), ('tg-Cyrl-TJ', 'Tajik (Cyrillic) - Tajikistan'), ('tzm', 'Tamazight (Latin)'), ('tzm-Latn', 'Tamazight (Latin), Latn'), ('tzm-Latn-DZ', 'Tamazight (Latin) - Algeria'), ('ta', 'Tamil'), ('ta-IN', 'Tamil - India'), ('ta-MY', 'Tamil - Malaysia'), ('ta-SG', 'Tamil - Singapore'), ('ta-LK', 'Tamil - Sri Lanka'), ('twq', 'Tasawaq'), ('twq-NE', 'Tasawaq - Niger'), ('tt', 'Tatar'), ('tt-RU', 'Tatar - Russia'), ('te', 'Telugu'), ('te-IN', 'Telugu - India'), ('teo', 'Teso'), ('teo-KE', 'Teso - Kenya'), ('teo-UG', 'Teso - Uganda'), ('th', 'Thai'), ('th-TH', 'Thai - Thailand'), ('bo', 'Tibetan'), ('bo-IN', 'Tibetan - India'), ('bo-CN', "Tibetan - People's Republic of China"), ('tig', 'Tigre'), ('tig-ER', 'Tigre - Eritrea'), ('ti', 'Tigrinya'), ('ti-ER', 'Tigrinya - Eritrea'), ('ti-ET', 'Tigrinya - Ethiopia'), ('to', 'Tongan'), ('to-TO', 'Tongan - Tonga'), ('ts', 'Tsonga'), ('ts-ZA', 'Tsonga - South Africa'), ('tr', 'Turkish'), ('tr-CY', 'Turkish - Cyprus'), ('tr-TR', 'Turkish - Turkey'), ('tk', 'Turkmen'), ('tk-TM', 'Turkmen - Turkmenistan'), ('uk', 'Ukrainian'), ('uk-UA', 'Ukrainian - Ukraine'), ('hsb', 'Upper Sorbian'), ('hsb-DE', 'Upper Sorbian - Germany'), ('ur', 'Urdu'), ('ur-IN', 'Urdu - India'), ('ur-PK', 'Urdu - Islamic Republic of Pakistan'), ('ug', 'Uyghur'), ('ug-CN', "Uyghur - People's Republic of China"), ('uz-Arab', 'Uzbek - Perso-Arabic'), ('uz-Arab-AF', 'Uzbek - Perso-Arabic, Afghanistan'), ('uz-Cyrl', 'Uzbek (Cyrillic)'), ('uz-Cyrl-UZ', 'Uzbek (Cyrillic) - Uzbekistan'), ('uz', 'Uzbek (Latin)'), ('uz-Latn', 'Uzbek (Latin), Latn'), ('uz-Latn-UZ', 'Uzbek (Latin) - Uzbekistan'), ('vai', 'Vai'), ('vai-Vaii', 'Vai, Vaii'), ('vai-Vaii-LR', 'Vai - Liberia'), ('vai-Latn-LR', 'Vai (Latin) - Liberia'), ('vai-Latn', 'Vai (Latin)'), ('ca-ES-valencia', 'Valencian - Spain'), ('ve', 'Venda'), ('ve-ZA', 'Venda - South Africa'), ('vi', 'Vietnamese'), ('vi-VN', 'Vietnamese - Vietnam'), ('vo', 'Volapük'), ('vo-001', 'Volapük - World'), ('vun', 'Vunjo'), ('vun-TZ', 'Vunjo - Tanzania'), ('wae', 'Walser'), ('wae-CH', 'Walser - Switzerland'), ('cy', 'Welsh'), ('cy-GB', 'Welsh - United Kingdom'), ('wal', 'Wolaytta'), ('wal-ET', 'Wolaytta - Ethiopia'), ('wo', 'Wolof'), ('wo-SN', 'Wolof - Senegal'), ('xh', 'Xhosa'), ('xh-ZA', 'Xhosa - South Africa'), ('yav', 'Yangben'), ('yav-CM', 'Yangben - Cameroon'), ('ii', 'Yi'), ('ii-CN', "Yi - People's Republic of China"), ('yo', 'Yoruba'), ('yo-BJ', 'Yoruba - Benin'), ('yo-NG', 'Yoruba - Nigeria'), ('dje', 'Zarma'), ('dje-NE', 'Zarma - Niger'), ('zu', 'Zulu'), ('zu-ZA', 'Zulu - South Africa')], default='en', help_text='Required if type is "Subtitle"', max_length=50),
        ),
    ]
