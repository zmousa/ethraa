from app.AWNDatabaseManagement import wn

# item	11269
# link	18522
# word	23481
# form	16998
summary = wn.summary()
print(summary)

# ¯\_(ツ)_/¯
result = wn.get_synsets_from_word('فرح')
print(result)