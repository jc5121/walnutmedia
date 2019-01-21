# -*- coding=UTF-8 -*-
import re

str = 'Facebook Installs::Walnut_CF_IOS_VO_Asia+ZA+SouthAmerica_Mix_1207_D ' \
      '(23843075926030026)::IOS_VO_Asia+ZA+SouthAmerica_PurAmnt≥90+lal+1%_Multi-Theme1 ' \
      '4:5 (23843075926340026)'

str2 = "Facebook Installs::Walnut_CF_Android_AEO_US+CA_Mix_1207_D (23843215640470257)::Android_AEO_US+CA_PurFreqâ‰¥5+lal+1%_Tiger (23843215640910257)::display"

str3  = "Facebook Installs::Walnut_CF_IOS_VO_Asia+ZA+SouthAmerica_Mix_1207_D (23843075926030026)"

str4 = "Off-Facebook Installs::Walnut_CF_US/CA_IOS_AEO_CBO_Pur≥Sum-181205_J (23843144636400491)::Lookalike (CA, US, 1%) - pur ios sum ≥ Multi-Theme1 1:1 (23843144636410491)::Multi-Theme1 1:1 (23843144636390491)"

str5 = "Off-Facebook Installs::Walnut_CF_US/CA_IOS_AEO_CBO_Pur≥Sum-181205_J (23843144636400491)::Lookalike (CA, US, 1%) - pur ios sum ≥ Multi-Theme1 1:1 (23843144636410491)"
#print str2.split(' ')[-1][1:-1]

#print str.split('::')[-1].split(' ')[0]

#print str3.split('::')[1].split(' ')[0]

#print str2.split('::')[2].split(' ')[0][1:-1]

print str4.split('::')[2].split(' ')[-1]
a = str4.split('::')[2].split(' ')[-1]
b = str4.split('::')[2].split(' ')[-1][1:-1]
print b
print str4.split('::')[2].replace(a, '').strip()

print str4.split('::')[3].split(' ')[-1]
c = str4.split('::')[3].split(' ')[-1]
print str4.split('::')[3].replace(c, '').strip()


23843144645260491
23843144645270491
