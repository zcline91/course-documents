\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{../homework}[2022/04/09 First Attempt]

% \newcommand{\rulecolor}{black}

\RequirePackage{fancyhdr}
\RequirePackage{calc}
% \RequirePackage{xcolor}
% \DeclareOption{blue}{\renewcommand{\rulecolor}{blue}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[letterpaper]{article}
\RequirePackage[margin=1in]{geometry}

\def\coursenumber#1{\gdef\@coursenumber{#1}}
\def\@coursenumber{\@latex@warning@no@line{No \noexpand\coursenumber given}}
\def\coursename#1{\gdef\@coursename{#1}}
\def\@coursename{\@latex@warning@no@line{No \noexpand\coursename given}}
\def\semester#1{\gdef\@semester{#1}}
\def\@semester{\@latex@warning@no@line{No \noexpand\semester given}}
\def\instructor#1{\gdef\@instructor{#1}}
\def\@instructor{\@latex@warning@no@line{No \noexpand\instructor given}}

\def\@maketitle{%
  %\newpage %\null  %\vskip 2em%
  \begin{center}%
    {\Large \@title } \\[-0.6em] %
    % {\color{\rulecolor} \rule{\maxof{\maxof{\widthof{\Large \@title}}{\widthof{\@coursenumber{} -- \@coursename{}}}}{\widthof{\@semester{} -- \@instructor{}}} + 2em}{.5pt}} \\[-0.5em] %
    \rule{\maxof{\maxof{\widthof{\Large \@title}}{\widthof{\@coursenumber{} -- \@coursename{}}}}{\widthof{\@semester{} -- \@instructor{}}} + 2em}{.5pt} \\[-0.5em] %
    \vskip 1ex%
    {\small%
      \@coursenumber{} -- \@coursename{} \\ %
      \@semester{} -- \@instructor{}%
    }%
  \end{center}%
  \par   \vskip 1.5em}

\setlength{\headheight}{15pt}

\AtBeginDocument{%
\edef\mytitle{\@title}
}

\pagestyle{fancy}
\fancyhf{}
\rhead{\textbf{\mytitle}}
\lhead{\@coursenumber{} -- \@coursename{}}
\cfoot{\thepage}
