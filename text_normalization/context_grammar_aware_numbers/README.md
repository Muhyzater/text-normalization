# Problem Overview
- #### The problem we face here. We need to specify the gender of the number when converting it from a numeric-number(20,30,40,50,...) to text-number(عشرون-عشرين,ثلاثون-ثلاثين.....).
  This problem in Arabic is called [Context Grammar Aware Numbers](https://ar.islamway.net/article/60343/%D9%82%D9%88%D8%A7%D8%B9%D8%AF-%D9%83%D8%AA%D8%A7%D8%A8%D8%A9-%D8%A7%D9%84%D8%A3%D8%B9%D8%AF%D8%A7%D8%AF-%D8%A8%D8%AD%D8%B1%D9%88%D9%81-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9).


# How it works
  Mawdoo3 Tashkeel model use the Arabic grammar for add Tashkeel to the word. 
  So, In context grammar gender aware project we can  replace the number with text number [20,عشرون] 
  then remove the `ون` then send the sentence to the Tashkeel model 
  then detect the last character Tashkeel in the word if `فتحه` or `كسره` or `ضمه`
  
  Example:
  يتكون فريقي فى العمل من 20 مهندساً
  ```
  Replace 20 with عشرون
  يتكون فريقي فى العمل من عشرون مهندساً
  
  Remove  ون
  يتكون فريقي فى العمل من عشر مهندساً
 
 Send sentence to Tashkeel model :
يَتَكَونُ فَرِيقِي فَى الْعَمَلِ مِنْ عَشَرِ مُهَنْدِسَا  
```
The last char in عشر is  ر  with كسره .So, عشر is مجرور

# Model Used
  - ## Mawdoo3 Tasheel Model
  - ## [Mishkal Model](https://github.com/linuxscout/mishkal)

# Mishkal Vs. Tashkeel
  | Mishkal  | Mishkal |
  | ------------- | ------------- |
  |  ركب القطار عشرين مسافرًا  | ركب القطار عشرين مسافرًا  |
  |   قرأت خمس و أربعين قصة |  قرأت خمس و أربعين قصة |
  |  حفظت إثنتين و ثلاثين بيتًا من الشعر  |  حفظت إثنتين و ثلاثين بيتًا من الشعر |
  |  حضر ستين طالب  |  حضر ستون طالب |
  |  زارني ثلاثة و عشرون ولدا زارتني ثلاث و عشرون طالبةً  | زارني ثلاثة و عشرين ولدا زارتني ثلاث و عشرون طالبةً  |
  |  التقيتُ ثلاثة و عشرين ولدا التقيت ثلاث و عشرون طالبةً  |  التقيتُ ثلاثة و عشرين ولدا التقيت ثلاث و عشرون طالبةً |
  |  سلّمْتُ ثلاثة و عشرين ولدا سلّمْتُ على ثلاث و عشرون طالبةً  | سلّمْتُ ثلاثة و عشرين ولدا سلّمْتُ على ثلاث و عشرون طالبةً  |
  |  عندي إثنتين و خمسين كتابًا عندي إثنان و خمسون مجلةً  |  عندي إثنتين و خمسين كتابًا عندي إثنان و خمسون مجلةً |
  |  اقتنيْتُ إثنتين و خمسين كتابًا اقتنيْتُ إثنان و خمسون مجلةً  |  اقتنيْتُ إثنتين و خمسين كتابًا اقتنيْتُ إثنان و خمسون مجلةً |
  |  اطّلعْتُ على إثنتين و خمسين كتابًا اطّلعْتُ على إثنان و خمسون مجلةً  |  اطّلعْتُ على إثنتين و خمسين كتابًا اطّلعْتُ على إثنان و خمسون مجلةً |
  |   حضرَ الحفلة تسعة و تسعون ولدا حضرَ الحفلة تسع و تسعين طالبةً |  حضرَ الحفلة تسعة و تسعين ولدا حضرَ الحفلة تسع و تسعين طالبةً |
  |  التقيْتُ تسعة و تسعين مسافرا التقيْتُ تسع و تسعون طالبةًً  |  التقيْتُ تسعة و تسعين مسافرا التقيْتُ تسع و تسعون طالبةًً |
  |  استمعْتُ إلى تسعة و تسعين مسافرا استمعْتُ إلى تسع و تسعون طالبةً  | استمعْتُ إلى تسعة و تسعون مسافرا استمعْتُ إلى تسع و تسعون طالبةً  |
  
  Mishkal & Tashkeel are same in 10 sentences and different in 4 sentences.
  
  - ## Different sentences
  | Mishkal  | Mishkal |
  | ------------- | ------------- |
  |  حضر ستين طالب  |  حضر ستون طالب |
  |  زارني ثلاثة و عشرون ولدا زارتني ثلاث و عشرون طالبةً  | زارني ثلاثة و عشرين ولدا زارتني ثلاث و عشرون طالبةً  |
  |   حضرَ الحفلة تسعة و تسعون ولدا حضرَ الحفلة تسع و تسعين طالبةً |  حضرَ الحفلة تسعة و تسعين ولدا حضرَ الحفلة تسع و تسعين طالبةً |
  |  استمعْتُ إلى تسعة و تسعين مسافرا استمعْتُ إلى تسع و تسعون طالبةً  | استمعْتُ إلى تسعة و تسعون مسافرا استمعْتُ إلى تسع و تسعون طالبةً  |
  
  Mishkal is better than Tashkeel in the 4 different sentences.


# Future work
  
# Resources
- ## [Mishkal Model](https://github.com/linuxscout/mishkal)
