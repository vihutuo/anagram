import flet as ft
import mymodules.utils as utils
import threading
#import random

from flet import Page, Text


def IndexView(page, params):

  def user_letter_box_clicked(e):
    alphabet = e.control.text
    if alphabet != "":
      e.control.data.text = alphabet
      e.control.data.update()
      e.control.text = ""
      e.control.update()

  def word_letter_box_clicked(e):
    #e.control is the button that was clicked
    alphabet = e.control.text
    if alphabet != "":
      for x in row_user_letters.controls:
        if x.text == "":
          x.text = alphabet
          x.data = e.control
          x.update()
          e.control.text = ""
          e.control.update()
          break

  def NewGame():
    nonlocal chosen_word
    nonlocal score
    score = 0
    txt_score.value = score
    row_user_letters.controls.clear()
    row_word_letters.controls.clear()

    chosen_word = utils.GetRandomWord("data/7_letter_words.txt")
    chosen_word = utils.ShuffleString(chosen_word).upper()

    CreateUserLetterBoxes(len(chosen_word))
    CreateWordLetterBoxes(chosen_word)
    #print(chosen_word)
    txt_entered_words.value = ""
    page.update()

  def CreateWordLetterBoxes(word):
    for i in range(len(word)):
      btn_1 = ft.FilledButton(word[i],
                              width=40,
                              height=40,
                              on_click=word_letter_box_clicked,
                              style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=20),
                                padding=4))
      row_word_letters.controls.append(btn_1)

  def CreateUserLetterBoxes(length):
    for i in range(length):
      btn_1 = ft.OutlinedButton("",
                                width=40,
                                height=40,
                                on_click=user_letter_box_clicked,
                                style=ft.ButtonStyle(
                                  shape=ft.RoundedRectangleBorder(radius=7),
                                  padding=4))
      row_user_letters.controls.append(btn_1)

  def btn_question1_clicked(e):
    page.go("/question/1")

  def btn_question2_clicked(e):
    page.go("/question/2")

  def btn_simple_clicked(e):
    page.go("/simple_view")

  def hide_points():
    txt_points.opacity = 0
    txt_points.update()
    print("Hide points")

  def points_animation_end(e):
    print("Animation end")
    if txt_points.opacity != 0:
      threading.Timer(1, hide_points).start()

  #print("Animation end")

  #CLEAR BUTTON

  #e.control is the button that was clicked

  def clear_user_words(e):
    for x in row_user_letters.controls:
      alphabet = x.text
      if alphabet != "":
        x.data.text = alphabet
        x.data.update()
        x.text = ""
        x.update()

  def check_for_complete_word():
    #If word is properly formed return the word else returm empty string
    word = ""
    for x in row_user_letters.controls:
      if x.text == "":
        word += " "
      else:
        word += x.text
    word = word.rstrip()
    isspace = word.find(" ")

    if isspace == -1 and len(word) >= 3:
      return word
    else:
      return ""

  def restart_clicked(e):
    NewGame()

  def q_icon(e):

    def bs_dismissed(e):
      print("Dismissed!")

    def show_bs(e):
      bs.open = True
      bs.update()

    def close_bs(e):
      bs.open = False
      bs.update()

    bs = ft.BottomSheet(
      ft.Container(
        ft.Column(
          [
            ft.Text(
              """An anagram is a word or phrase that is formed by rearranging the letters of another word.
                    INSTRUCTION:
                    (1)The word should contain atleast Three(3) letters
                    (2)For each letter you will earn One(1) point
                    (3)BONUS POINT for Seven(7) letter words i.e 7+3 = 10 points 
                    
*TO GET COUPON ,YOUR SCORE SHOULD BE ATLEAST 20 POINTS*
                    """),
            ft.ElevatedButton("OK", icon="CHECK_ROUNDED", on_click=close_bs),
          ],
          tight=True,
        ),
        padding=10,
      ),
      open=True,
      on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)
    page.add(ft.ElevatedButton("Display bottom sheet", on_click=show_bs))

  def check_user_word(e):
    nonlocal score
    user_word = check_for_complete_word()
    print(user_word)
    if user_word == "":
      return
  #def definition(e):

    copy_chosen = str(chosen_word)
    valid = True
    #Check 1
    for c in user_word:
      if c not in copy_chosen:
        valid = False
        break
      copy_chosen = copy_chosen.replace(c, "", 1)
    #Check 2
    if valid:
      if user_word not in all_words:
        valid = False
    #Check 3
    if valid:
      if user_word in all_user_words:
        valid = False

    if valid:
      all_user_words.append(user_word)
      e.control.value = ""
      #e.control.value.update()
      txt_entered_words.value += "\t\t\t" + user_word
      txt_entered_words.update()
      if len(user_word) == 7:
        points = int(10)
      else:
        points = len(user_word)
      score += points

      txt_score.value = score
      txt_score.update()
      txt_points.value = "+" + str(points)
      txt_points.opacity = 1

      txt_points.update()

    print(valid)

  #####Game variables############
  score = 0
  chosen_word = ""
  all_user_words = []
  all_words = utils.GetAllWords("data/3_letter_plus_words.txt")

  appbar = ft.AppBar(title=ft.Text(
    value="Anagram ",
    weight=ft.FontWeight.BOLD,
    color="#618685",
  ),
                     bgcolor=ft.colors.SURFACE_VARIANT,
                     center_title=True,
                     actions=[
                       ft.IconButton(ft.icons.RESTART_ALT,
                                     on_click=restart_clicked,
                                     icon_color="Green"),
                       ft.IconButton(ft.icons.QUESTION_MARK_OUTLINED,
                                     on_click=q_icon,
                                     icon_color="Blue"),
                     ])

  #score
  txt_score = ft.Text(value="0",
                      size=22,
                      weight=ft.FontWeight.BOLD,
                      color="#92a8d1")
  txt_display_score = ft.Text(text_align=ft.TextAlign.RIGHT,
                              value="Score : ",
                              size=22,
                              weight=ft.FontWeight.BOLD,
                              color="#92a8d1")

  row_score = ft.Row(controls=[txt_display_score, txt_score],
                     alignment=ft.MainAxisAlignment.END)

  page.bgcolor = ft.colors.BLUE_ACCENT
  line_1 = ft.Divider(height=1, color=ft.colors.SECONDARY_CONTAINER)
  row_user_letters = ft.Row()
  txt_entered_words = ft.Text("")
  btn_submit = ft.ElevatedButton("Submit", on_click=check_user_word)
  btn_clear = ft.ElevatedButton(" Clear", on_click=clear_user_words)

  team_name = ft.Text(
    value="Created by :  Lendina, Shubham & Sir Vihutuo(Teacher), LSHSS. \nMake as many 3 letter or longer words.",
    size=15,
    opacity=0.60,
    color="#b2b2b2")

  row_submit_clear = ft.Row(controls=[btn_submit, btn_clear],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            width=350)

  row_word_letters = ft.Row()
  txt_points = ft.Text("",
                       animate_opacity=600,
                       opacity=0,
                       on_animation_end=points_animation_end)

  col_left = ft.Column(controls=[
    ft.Row(controls=[row_user_letters, txt_points]), row_word_letters,
    row_submit_clear
  ])
  #col_right=ft.Column(controls=[txt_entered_words])
  #row_main = ft.Row(controls=[col_left,col_right],spacing=100,
  #vertical_alignment=ft.CrossAxisAlignment.START)
  page.views.append(
    ft.View("/", [
      appbar, row_score, line_1, col_left, txt_entered_words,
      ft.Container(
        content=team_name,
        border=ft.border.only(
          top=ft.border.BorderSide(1, ft.colors.SECONDARY_CONTAINER)),
        margin=ft.margin.only(top=250))
    ]))
  page.update()
  print(page.client_user_agent,page.client_ip,page.platform)
  NewGame()
  

