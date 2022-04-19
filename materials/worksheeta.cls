%-------------Identification-------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{worksheeta}[2022/04/16]

%--------------Initial Code--------------
\RequirePackage{xcolor}
\RequirePackage{ifthen}
\newboolean{boxed@solutions}
\newcommand{\solution@color}

%---------Declaration of Options---------
\DeclareOption{blue-solutions}{\AtEndOfClass{\SolutionEmphasis{\color{blue}}}}
\DeclareOption{red-solutions}{\AtEndOfClass{\SolutionEmphasis{\color{red}}}}
\DeclareOption{boxed-solutions}{\setboolean{boxed@solutions}{true}}
\DeclareOption{no-boxed-solutions}{\setboolean{boxed@solutions}{false}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{exam}}

%----------Execution of Options----------
\ExecuteOptions{12pt, answers, no-boxed-solutions}
\ProcessOptions \relax

%-------------Package Loading------------
\LoadClass[letterpaper]{exam}
\RequirePackage{calc}

%----------------Main Code---------------

% Add some new maketitle options
\def\coursenumber#1{\gdef\@coursenumber{#1}}
\def\@coursenumber{\@latex@warning@no@line{No \noexpand\coursenumber given}}
\def\coursename#1{\gdef\@coursename{#1}}
\def\@coursename{\@latex@warning@no@line{No \noexpand\coursename given}}
\def\semester#1{\gdef\@semester{#1}}
\def\@semester{\@latex@warning@no@line{No \noexpand\semester given}}
\def\instructor#1{\gdef\@instructor{#1}}
\def\@instructor{\@latex@warning@no@line{No \noexpand\instructor given}}
% Save maketitle options for use in header
\AtBeginDocument{\let\thetitle\@title}
\AtBeginDocument{\let\theauthor\@author}
\AtBeginDocument{\let\thedate\@date}
\AtBeginDocument{\let\thecoursenumber\@coursenumber}
\AtBeginDocument{\let\thecoursename\@coursename}
\AtBeginDocument{\let\thesemester\@semester}
\AtBeginDocument{\let\theinstructor\@instructor}

% Set header and footer
\pagestyle{headandfoot}
% \firstpageheader{\thecoursenumber \\ \thecoursename}{\Large \thetitle}{\thesemester \\ \theinstructor}
% \firstpagefooter{}{\thepage}{}
\runningheadrule
\runningheader{\thecoursenumber}{\textbf{\thetitle}}{\thesemester}
% \runningfooter{}{\thepage}{}
\footer{}{Page \thepage{} of \numpages}{}

% Make title and set footer for first page
\AtBeginDocument{\maketitle \thispagestyle{headandfoot}}

% Style solutions
\renewcommand{\solutiontitle}{\noindent\textbf{Solution:}\par\noindent}
\ifthenelse{\boolean{boxed@solutions}}{}{\colorsolutionboxes \definecolor{SolutionBoxColor}{HTML}{FFFFFF}}

% Custom Title
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
  \par   \vskip 1em}
